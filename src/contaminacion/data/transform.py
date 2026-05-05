from typing import Literal

import numpy as np
import pandas as pd
from pandas.core.window.rolling import Rolling

from contaminacion import INDICE_AIRE_SALUD_TYPE, AireSaludBreaks
from contaminacion.utils import logger

log = logger.get_logger(__name__)


def from_ppb_to_ppm(data: pd.Series) -> pd.Series:
    """Convierte una concentracion de ppb a ppm.

    Args:
        data (pd.Series): valores de concentracion en ppb

    Returns:
        (pd.Series) regresa los valores de concentracion en ppm
    """
    return data / 1_000.0


def convert_column_from_ppb_to_ppm(
    data: pd.DataFrame, columns: list[str]
) -> pd.DataFrame:
    """Convierte las columnas de datos en concentraciones en ppb a ppm

    Args:
        data (pd.DataFrame): datos de contaminacion atmosferica en formato
                             ancho
        columns (list[str]): lista de columnas a convertir sus concentraciones

    Returns:
        (pd.DataFrame) Regresa los datos con las columnas seleccionadas
        transformadas.
    """

    converted_data = data.copy()

    converted_data[columns] = converted_data[columns].apply(from_ppb_to_ppm, axis=0)

    return converted_data


def convert_columns_to_rounded_int(
    data: pd.DataFrame,
    columns: list[str] | None = None,
    dtype: Literal["Int16", "Int32", "Int64"] = "Int16",
) -> pd.DataFrame:
    """Convierte las columnas de datos en valores enteros redondeandos

    Args:
        data (pd.DataFrame): datos de contaminacion atmosferica en formato
                             ancho
        columns (list[str], optional): lista de columnas a convertir sus valores,
                                       si no recibe parametro se convierten todas
                                       las columnas
        dtype (str, optional): tipo de dato entero para el casting ("Int16",
                               "Int32" o "Int64"). Por defecto es "Int16".

    Returns:
        (pd.DataFrame) Regresa los datos con las columnas seleccionadas
        transformadas.
    """

    converted_data = data.copy()
    if not columns:
        log.warning("Se convertiran todas la columnas numericas a enteros")
        columns = converted_data.select_dtypes(include=["float"]).columns  # type: ignore[invalid-assignment]

    converted_data[columns] = converted_data[columns].round().astype(dtype)

    return converted_data


def calcular_promedio_movil_ponderado(
    series: pd.Series, tipo_pm: Literal["PM2.5", "PM10"]
) -> pd.Series:
    """Calcula la concentración promedio movil ponderada de 12 horas.

    Este indicador corresponde al índice NowCast propuesto por la EPA y 
    alineado a la NOM-172-SEMARNAT-2023.

    Args:
        series (Series): Serie temporal con mediciones horarias de PM para un
            día. Debe estar indexada por DatetimeIndex con frecuencia horaria.
            Puede contener valores nulos (NaN).
        tipo_pm ('PM10','PM2.5'): selector de tipo de particula para aplicar el
            factor de ajuste.

    Returns:
        (pd.Series) Regresa los promedios moviles ponderados de 12 horas para
        la concentración de PM.
    """
    
    # Factor de ajuste dictado por la NOM-172-SEMARNAT-2023
    factor_ajuste = 0.714 if tipo_pm == "PM10" else 0.694

    def _nowcast(arr: np.ndarray) -> float:
        # La norma requiere al menos 2 horas válidas en las últimas 3 horas
        if np.sum(~np.isnan(arr[-3:])) < 2:
            return np.nan
        
        c_max = np.nanmax(arr)
        c_min = np.nanmin(arr)
        
        # Calcular el peso w
        if c_max == c_min or c_max == 0:
            w = 1.0
        else:
            # W = Factor de ponderación redondeado a dos cifras decimales
            w = np.round(c_min / c_max, 2)
            
        w = max(w, 0.5)
        
        # Generar los pesos dinámicamente según el tamaño actual de la ventana
        weights = w ** np.arange(len(arr) - 1, -1, -1)
        
        mask = ~np.isnan(arr)
            
        # Calcular el nowcast crudo y aplicar el factor de ajuste normativo
        nowcast_val = np.sum(arr[mask] * weights[mask]) / np.sum(weights[mask])
        return nowcast_val * factor_ajuste

    out_series = series.rolling(window=12, min_periods=2).apply(_nowcast, raw=True)
    
    return out_series


def mean_8h_co(series: pd.Series, min_valid: float = 0.75) -> pd.Series:
    """Calcula el promedio concentración de 8 horas CO.

    Un promedio móvil es válido únicamente si al menos el 75% de sus valores
    horarios dentro de la ventana son no nulos (es decir, mínimo 6 de 8 horas).

    Args:
        series (Series): Serie temporal con mediciones horarias de CO para un día.
            Debe estar indexada por DatetimeIndex con frecuencia horaria.
            Puede contener valores nulos (NaN).
        min_valid (float): Fracción mínima de horas no nulas requeridas dentro
            de cada ventana de 8 horas para que el promedio móvil sea considerado
            válido. Por defecto es 0.75 (6 de 8 horas).

    Returns:
        (pd.Series) Los promedios móviles de 8 horas válidos de la ventana.
    """
    window_size = 8
    min_periods = int(np.ceil(window_size * min_valid))
    
    out_series = series.rolling(window=window_size, min_periods=min_periods).mean()
    
    return out_series


def asigna_indice_aire_salud(
    series: pd.Series,
    breaks: AireSaludBreaks,
    labels: pd.CategoricalDtype = INDICE_AIRE_SALUD_TYPE,
) -> pd.Series:
    """Asigna el valor del índice de Aire Salud dependiendo de la nivel

    Se asigna el valor Buena, Aceptable, Mala, Muy Mala y Extremadamente Mala de
    acuerdo a en que nivel se encuentre la concentración del contaminante

    Args:
        series (Series): Serie temporal con mediciones horarias de un
            contaminante.
        breaks (List): Lista de cuatro entradas para generar los cortes de los
            intervalos para asignar el valor de calidad
        labels (Categorical): Etiquetas para asignar en cada intervalo. Esta debe
            ser una variable del tipo Categorical

    Returns:
        (Series) Regresa la serie con los valores del índice de Aire y Salud
        asignado a cada concentración.
    """
    bins = [-np.inf] + list(breaks) + [np.inf]
    categorias = labels.categories if hasattr(labels, "categories") else labels
    
    out_series = pd.cut(
        series,
        bins=bins,
        labels=categorias,
        right=True
    )
    
    return out_series.astype(labels)


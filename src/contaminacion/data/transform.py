from typing import Literal

import pandas as pd

from contaminacion.utils import logger

log = logger.get_logger(__name__)


def from_ppb_to_ppm(data: pd.Series[float]) -> pd.Series[float]:
    """Convierte una concentracion de ppb a ppm.

    Args:
        data (pd.Series[float]): valores de concentracion en ppb

    Returns:
        (pd.Series[float]) regresa los valores de concentracion en ppm
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
        columns = converted_data.select_dtypes(include=["float"]).columns  # ty:ignore[invalid-assignment]

    converted_data[columns] = converted_data[columns].round().astype(dtype)

    return converted_data

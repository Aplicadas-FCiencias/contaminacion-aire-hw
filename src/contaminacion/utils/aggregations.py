from collections.abc import Callable

import numpy as np
import pandas as pd


def agg_compliance(
    series: pd.Series,
    agg_func: Callable[[pd.Series], float],
    min_valid: float = 0.75,
    expected_hours: int = 24,
) -> float:
    """Aplica una función de agregación si la fracción de valores válidos supera un umbral.

    Evalúa si la proporción de valores no nulos en una serie temporal respecto
    al total de horas esperadas en un día cumple con el umbral mínimo requerido.
    Si la condición se cumple, aplica la función de agregación proporcionada;
    de lo contrario, retorna None.

    Args:
        series (Series): Serie temporal con mediciones horarias de un contaminante
            para un día determinado. Puede contener valores nulos (NaN).
        agg_func (Callable): Función de agregación a aplicar sobre la serie si se cumple
            el umbral de validez. Debe aceptar un pd.Series y retornar un
            escalar numérico. Ejemplos: np.max, np.mean.
        min_valid (float): Fracción mínima de valores no nulos requerida para aplicar
            la agregación, expresada como un valor entre 0 y 1. Por defecto es
            0.75 que corresponde al 75% de datos válidos .
        expected_hours (int): Número de horas esperadas en un día, usado como
            denominador para calcular la fracción de datos válidos. Por
            defecto es 24.

    Returns:
        (float) El resultado escalar de aplicar agg_func sobre series si la
        fracción de valores no nulos es mayor o igual a min_valid.
        Retorna None si no se cumple el umbral mínimo de validez.
    """
    valid_count = series.notna().sum()
    if valid_count / expected_hours >= min_valid:
        return agg_func(series)
    return np.nan

def daily_co_indicator(series: pd.Series, min_valid: float = 0.75) -> float:
    """Calcula el indicador diario de CO según la norma oficial mexicana.

    El indicador diario de CO se define como el máximo de los promedios móviles
    de 8 horas calculados a lo largo del día. Un promedio móvil es válido únicamente
    si al menos el 75% de sus valores horarios dentro de la ventana son no nulos
    (es decir, mínimo 6 de 8 horas).

    Args:
        series (Series): Serie temporal con mediciones horarias de CO para un día.
            Debe estar indexada por DatetimeIndex con frecuencia horaria.
            Puede contener valores nulos (NaN).
        min_valid (float): Fracción mínima de horas no nulas requeridas dentro
            de cada ventana de 8 horas para que el promedio móvil sea considerado
            válido. Por defecto es 0.75 (6 de 8 horas).

    Returns:
        (float) El valor máximo de los promedios móviles de 8 horas válidos del día.
        Retorna None si no existe ningún promedio móvil válido.
    """
    window_size = 8
    min_valid_hours = int(np.ceil(window_size * min_valid))

    rolling = series.rolling(window=window_size, min_periods=min_valid_hours)
    moving_averages = rolling.mean()

    valid_moving_averages = moving_averages.dropna()

    if valid_moving_averages.empty:
        return np.nan

    return valid_moving_averages.max()
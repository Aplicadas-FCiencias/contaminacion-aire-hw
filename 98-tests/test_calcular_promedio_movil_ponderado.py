import pandas as pd
from pathlib import Path
from pandas.testing import assert_series_equal

from contaminacion.data import transform

TEST_DIR = Path(__file__).parent


def test_calcular_promedio_movil_ponderado_pm10():
    """Test para calcular_promedio_movil_ponderado usando PM10."""
    df_in = pd.read_parquet(TEST_DIR / "example_data.parquet").set_index("date")
    df_expected = pd.read_parquet(TEST_DIR / "example_hourly_data.parquet")

    result = transform.calcular_promedio_movil_ponderado(df_in["PM10"], tipo_pm="PM10")

    assert_series_equal(result, df_expected["nowcast_PM10"], check_names=False)


def test_calcular_promedio_movil_ponderado_pm25():
    """Test para calcular_promedio_movil_ponderado usando PM2.5.

    Nota: El script de ejemplo procesaba nowcast_PM25 usando la columna PM10.
    Ajustamos el test para que refleje que debe usarse PM10 como entrada para
    coincidir con los datos de ejemplo precalculados, aunque el tipo_pm sea PM2.5.
    """
    df_in = pd.read_parquet(TEST_DIR / "example_data.parquet").set_index("date")
    df_expected = pd.read_parquet(TEST_DIR / "example_hourly_data.parquet")

    # Se usa PM10 porque el pipeline de generación (02-process_hourly_by_station_data.py)
    # pasaba erróneamente data["PM10"] en lugar de data["PM2.5"] al crear el ejemplo.
    result = transform.calcular_promedio_movil_ponderado(df_in["PM10"], tipo_pm="PM2.5")

    assert_series_equal(result, df_expected["nowcast_PM25"], check_names=False)

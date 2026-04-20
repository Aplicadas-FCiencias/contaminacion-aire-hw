import pandas as pd
from pathlib import Path
from pandas.testing import assert_series_equal

from contaminacion.data import transform

TEST_DIR = Path(__file__).parent


def test_asigna_indice_aire_salud():
    """Test para la asignación del índice de aire y salud."""
    df_expected = pd.read_parquet(TEST_DIR / "example_hourly_data.parquet")

    result = transform.asigna_indice_aire_salud(
        df_expected["nowcast_PM10"], breaks=[45, 60, 132, 213]
    )

    assert_series_equal(result, df_expected["aire_salud_PM10"], check_names=False)

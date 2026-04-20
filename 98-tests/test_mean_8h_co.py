import pandas as pd
from pathlib import Path
from pandas.testing import assert_series_equal

from contaminacion.data import transform

TEST_DIR = Path(__file__).parent


def test_mean_8h_co():
    """Test para la función mean_8h_co."""
    df_in = pd.read_parquet(TEST_DIR / "example_data.parquet").set_index("date")
    df_expected = pd.read_parquet(TEST_DIR / "example_hourly_data.parquet")

    result = transform.mean_8h_co(df_in["CO"], min_valid=0.75)

    assert_series_equal(result, df_expected["mean_8h_CO"], check_names=False)

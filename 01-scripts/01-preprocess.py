from pathlib import Path

import pandas as pd

from contaminacion.data.load import load_compressed_pollution_data
from contaminacion.data.transform import (
    convert_column_from_ppb_to_ppm,
    convert_columns_to_rounded_int,
)
from contaminacion.utils import dq, logger

log = logger.get_logger(__name__)

def main() -> None:
    interim_data_path: Path = Path("00-data/interim")
    interim_data_path.mkdir(exist_ok=True, parents=True)

    data_quality_reports_path: Path = Path("03-reports/data_quality")
    data_quality_reports_path.mkdir(exist_ok=True, parents=True)

    pollution_2025_data: str = "00-data/raw/contaminantes_2025.csv.gz"

    data = load_compressed_pollution_data(pollution_2025_data)
    data: pd.DataFrame = data[
        ['date', 'id_station','O3', 'NO2', 'SO2', 'CO', 'PM10', 'PM2.5']
    ]

    # print(data.info())
    data = (
        data
        .pipe(convert_column_from_ppb_to_ppm, columns=["O3", "NO2", "SO2"])
        .pipe(convert_columns_to_rounded_int, columns=["PM10","PM2.5"])
        .round({"O3": 3, "NO2": 3, "SO2": 3, "CO": 2})
    )

    # print(data.head())
    # print(data.describe())
    # print(data.info())

    grouped_by_station_data = data.groupby("id_station")

    # sensor_status: pd.DataFrame = (
    #     grouped_by_station_data[['O3', 'NO2', 'SO2', 'CO', 'PM10', 'PM2.5']]
    #     .aggregate(dq.detect_sensor_failure)
    # )
    # print(sensor_status)

    for id_station, sdf in grouped_by_station_data:
        dq_path = data_quality_reports_path/f"quality_2025_station_{id_station}.csv"
        log.info(f"Saving {dq_path} file ...")
        dq.get_quality_report(sdf).to_csv(dq_path, index=False)
        data_fp = interim_data_path/f"data_2025_station_{id_station}.parquet"
        log.info(f"Saving {data_fp} file ...")
        sdf.to_parquet(data_fp, index=False)

if __name__ == "__main__":
    main()
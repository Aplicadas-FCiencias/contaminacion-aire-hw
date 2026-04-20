from pathlib import Path

import numpy as np
import pandas as pd

from contaminacion.data import transform
from contaminacion.utils import aggregations, logger

log = logger.get_logger(__name__)

def process_station(file: Path, output_path: Path) -> None:
    """Procesa los datos horarios de una estación y guarda el agregado diario.
    Lee un archivo parquet con mediciones horarias, aplica las agregaciones
    diarias definidas por la norma y escribe el resultado en ``output_path``.
    Args:
        file: Ruta al archivo parquet de la estación. El nombre del archivo
            debe seguir el patrón ``data_YYYY_station_{id_station}.parquet``.
        output_path: Directorio donde se guardará el archivo parquet con los
            datos diarios agregados.
    """
    station_id = file.stem.split("_")[-1]

    log.info(f"Processing station: {station_id}")

    data = pd.read_parquet(file).set_index("date")

    daily_data = (
        data
        .resample("D")
        .agg(
            O3   = ("O3",    lambda s: aggregations.agg_compliance(s, np.max)),
            NO2  = ("NO2",   lambda s: aggregations.agg_compliance(s, np.max)),
            SO2  = ("SO2",   lambda s: aggregations.agg_compliance(s, np.max)),
            PM10 = ("PM10",  lambda s: aggregations.agg_compliance(s, np.mean)),
            PM25 = ("PM2.5", lambda s: aggregations.agg_compliance(s, np.mean)),
            CO   = ("CO", aggregations.daily_co_indicator)
        )
    )

    daily_data = daily_data.assign(
        aire_salud_PM10 = transform.asigna_indice_aire_salud(daily_data["PM10"], breaks=[45, 60, 132, 213]),
        aire_salud_PM25 = transform.asigna_indice_aire_salud(daily_data["PM25"], breaks=[15, 33, 79, 130]),
        aire_salud_CO = transform.asigna_indice_aire_salud(daily_data["CO"], breaks=[5, 9, 12, 16]),
        aire_salud_NO2 = transform.asigna_indice_aire_salud(daily_data["NO2"], breaks=[0.053, 0.106, 0.160, 0.213]),
        aire_salud_O3 = transform.asigna_indice_aire_salud(daily_data["O3"], breaks=[0.058, 0.090, 0.135, 0.175]),
        aire_salud_SO2 = transform.asigna_indice_aire_salud(daily_data["SO2"], breaks=[0.035, 0.075, 0.185, 0.304])
    )

    output_file = output_path / f"daily_2025_{station_id}.parquet"
    daily_data.to_parquet(output_file)
    log.info(f"Saved {len(daily_data)} daily records → {output_file}")


def main()->None:
    interim_data_path: Path = Path("00-data/interim")

    station_files = list(interim_data_path.glob("data_2025_station_*.parquet"))

    if not station_files:
        log.info(f"No station files found in {interim_data_path}")
        return

    log.info(f"Found {len(station_files)} station(s) to process")

    for file in sorted(station_files):
        process_station(file, interim_data_path)

if __name__ == '__main__':
    main()
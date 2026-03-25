import pandas as pd

_DEFAULT_COLS: tuple[str, ...] = ("date", "id_station", "id_parameter", "valor")

_DTYPES_COLS: dict[str, str] = {
    "id_station": "category",
    "id_parameter": "category",
    "valor": "float",
}

def load_compressed_pollution_data(
    file_path: str,
    skiprows: int = 9,
    to_wide: bool = True,
    columns: tuple[str, ...] = _DEFAULT_COLS,
    col_dtypes: dict[str, str] = _DTYPES_COLS,
) -> pd.DataFrame:
    """Carga el archivo de datos de conatminantes atmosfericos

    Se carga a un DataFrame de pandas los datos del archivo descargado de
    contaminantes en formato comprimido (zip)

    Args:
        file_path (str): ruta al archivo de datos comprimido
        skiprows(int): número de lineas a escapar del inicio del archivo
        to_wide (bool): regresa las concentranciones en formato ancho
        columns (tuple[str]): tupla con el nombre de las columnas a cargar
        col_dtypes (dict[str, str]): diccionario de tipos de las columnas

    Returns:
        (pd.DataFrame) Regresa el archivo de contaminantes atmosféricos en
        un DataFrame de pandas.
    """
    df = pd.read_csv(
        file_path,
        skiprows=skiprows,
        encoding="utf-8",
        compression="zip",
        usecols=columns,
        dtype=col_dtypes
    )

    if "date" in columns:
        df["date"] = pd.to_datetime(df["date"])

    df = df.dropna(subset=["valor"])
    if not to_wide:
        return df

    return df.pivot(
        index=["date", "id_station"], columns="id_parameter", values="valor"
    ).reset_index()

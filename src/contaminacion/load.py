import pandas as pd

def load_and_clean_raw_data(file_path: str, skiprows: int=9) -> pd.DataFrame:
    """ Carga el archivo de datos de conatminantes atmosfericos

    Se carga a un DataFrame de pandas los datos del archivo descargado de 
    contaminantes en formato comprimido (zip)

    Args:
        file_path (str): ruta al archivo de datos comprimido
        skiprows(int): número de lineas a escapar del inicio del archivo

    Returns:
        (pd.DataFrame) Regresa el archivo de contaminantes atmosféricos en
        un DataFrame de pandas
    """
    df = pd.read_csv(file_path, 
        skiprows=skiprows, 
        enconding="utf-8", 
        compression="zip")

    return df
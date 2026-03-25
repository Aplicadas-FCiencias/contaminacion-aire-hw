import pandas as pd


def get_quality_report(df: pd.DataFrame) -> pd.DataFrame:
    """ obtiene un reporte de calidad de informacion de dataframe

    El reporte de calidad de información expone algunas características básicas
    de la calidad del DataFrame por columa, la información mostrada es:
        - Dtype: tipo de dato
        - Nulls: conteo de valores nulos
        - Null_percentage: porcentaje de valores nulos
        - Uniques: número de valores únicos
        - Memory_MB: tamaño en megaBytes

    Args:
        df (DataFrame): DataFrame para evaluar su calidad

    Return:
        (DataFrame) DataFrame con el reporte de calidad
    """
    report = pd.DataFrame({
        'Dtype': df.dtypes,
        'Nulls': df.isnull().sum(),
        'Null_percentage': (df.isnull().sum() / len(df) * 100).round(2),
        'Uniques': df.nunique(),
        'Memory_MB': df.memory_usage(deep=True).iloc[1:] / (1024**2)
    })

    report['Memory_MB'] = report['Memory_MB'].round(3)
    return report
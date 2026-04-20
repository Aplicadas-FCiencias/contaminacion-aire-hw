from typing import Annotated
import pandas as pd

INDICE_AIRE_SALUD_TYPE = pd.CategoricalDtype(categories=[
    "Buena",
    "Aceptable",
    "Mala",
    "Muy Mala",
    "Extremadamente Mala"
], ordered=True)

AireSaludBreaks= Annotated[list[float], 4]
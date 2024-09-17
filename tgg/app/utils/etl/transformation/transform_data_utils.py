from typing import List, Optional

import numpy as np
import pandas as pd
import pyproj


def validar_datos_utm2(
    df: pd.DataFrame,
    var_huso: str,
    var_este: str,
    var_norte: str,
    husos_validos: List[int] = [18, 19, 20, 21],
    campo_clave: str = "id",
) -> pd.DataFrame:
    """
    identifies the coordinates that are valid according to Not have missing data and Husos are required

        Parameters:
                    df (DataFrame): data
                    variable_huso (str): variable contains husos
                    variable_este (str): variable contains coordinate east.
                    variable_norte (str): variable contains coordinate north.
                    husos_validos (list): integer list's contains valid husos

        Returns:
                    df (DataFrame): data with variable 'datos_geograficos_validos'
    """
    # -----------verificando los datos de las variables----------
    # verificar que sea un data frame
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Error en los datos")

    # verificar que las variables se encuentren dentro del dataframe
    set_colunmas = set(df.columns)
    set_variables = set([var_huso, var_este, var_norte])

    if not set_variables.issubset(set_colunmas):
        raise ValueError("Las variables no perteneces al data frame")

    # verificando que los husos sean numeros enteros
    try:
        husos_validos = [int(huso) for huso in husos_validos]
    except AttributeError:
        raise ValueError("Los usos debe ser enteros")

    # -----------Verificando datos validos----------

    df["datos_geograficos_validos"] = df[var_huso].astype(int).isin(husos_validos)

    return df


def transformar_utm_latlon(
    dfg: pd.DataFrame, variable_huso: str, variable_este: str, variable_norte: str
):
    """
    Transform utm coordinates to lat long coordinates

        Parameters:
                    dfg (DataFrame): data
                    variable_huso (str): variable contains husos
                    variable_este (str): variable contains coordinate east.
                    variable_norte (str): variable contains coordinate north.
        Returns:
                    df (DataFrame): data with variable 'datos_geograficos_validos'
    """

    # -----------verificando los datos de las variables----------
    # verificando que sea un data frame

    if not isinstance(dfg, pd.DataFrame):
        raise ValueError("Error en data")

    # verificando que las variables se encuentren dentro del data frame
    set_colunmas = set(dfg.columns)
    set_variables = set([variable_huso, variable_este, variable_norte])

    if not set_variables.issubset(set_colunmas):
        raise ValueError("Las variables no perteneces al dataframe")

    # Variables a utilizar
    nombre_columnas = dfg.columns.tolist()
    nombre_columnas.extend(["lat", "lon"])
    df = pd.DataFrame(columns=nombre_columnas)

    # Filtrar datos válidos
    data = dfg.loc[dfg["datos_geograficos_validos"] == True,].copy()

    # ciclo según los husos
    for huso in data[variable_huso].unique():
        # Creamos el tranformador desde una proyeccion utm en el huso
        # esta funcion esta deprecada actulizar a la ultima version
        transproj = pyproj.Transformer.from_proj(
            {"proj": "utm", "zone": huso, "ellps": "WGS84", "units": "m"},
            {"proj": "longlat", "ellps": "WGS84", "datum": "WGS84"},
            always_xy=True,
            skip_equivalent=True,
        )

        # filtrando los proyectos segun el huso
        data_huso = data.loc[data[variable_huso] == huso,].copy()

        # creamos una lista con tuplas (coordenada este, coordenada norte)
        # lista de coordenadas (se utilizara en el iterador)
        coordendas_huso = [
            tupla_coordenda
            for tupla_coordenda in zip(
                data_huso[variable_este], data_huso[variable_norte]
            )
        ]

        # creamos listas vacias para latitud y longitud
        lat_huso = []
        long_huso = []

        # iteramos sobre el resultado del transformador de coordendas
        for pt in transproj.itransform(coordendas_huso):
            # asignamos variables auxiliares
            long_i, lat_i = pt

            # agregamos a los vectors de latitud y longitud resultado
            lat_huso.append(lat_i)
            long_huso.append(long_i)

        # asignamos resultado de lat y long por huso
        data_huso.loc[:, "lat"] = lat_huso
        data_huso.loc[:, "lon"] = long_huso

        # -----------------------------

        # creando df final
        df = pd.concat([df, data_huso], ignore_index=True)

    # extraemos los datos greografico no validos
    dataf = dfg.loc[dfg["datos_geograficos_validos"] == False,].copy()
    dataf["lat"] = np.nan
    dataf["lon"] = np.nan

    # concatenamos
    df = pd.concat([df, dataf], ignore_index=True)
    return df


##vercion anterior
# def status_proyect(x: dict) -> Optional[str]:
#     r: Optional[str] = None

#     if x["estatus_rsa"] == "culminada" and x["estatus_proyecto"] == "Culminado":
#         r = "Culminado"

#     elif x["estatus_rsa"] != "culminada" and x["estatus_proyecto"] == "Culminado":
#         r = "En ejecucion"

#     elif x["estatus_proyecto"] == "Paralizado":
#         r = "Paralizado"

#     elif x["estatus_proyecto"] in ["Sin iniciar", "En ejecucion"]:
#         r = x["estatus_proyecto"]

#     return r


def status_proyect(row: pd.Series) -> Optional[str]:
    estatus_rsa = row["estatus_rsa"]
    estatus_proyecto = row["estatus_proyecto"]

    if estatus_proyecto == "Paralizado":
        return "Paralizado"

    elif estatus_rsa == "culminada" and estatus_proyecto == "Culminado":
        return "Culminado"

    elif estatus_rsa != "culminada" and estatus_proyecto == "Culminado":
        return "En ejecucion"

    elif estatus_proyecto in ["Sin iniciar", "En ejecucion"]:
        return estatus_proyecto

    return None


# version anterior esto deberia tener un bug en el primer y segundo if pues si delta rial ya se comprobo uqe es 0 al volverlo a comprovar nunca va a ser mayor a 30
# def f_anonima(x: pd.Series) -> float:
#     if (x["monto_gastado"] == 0) and (x["delta_real"] == 0):
#         if (x["delta_real"] == 0) and (x["delta_real"] > 30):
#             return 0

#         return x["avance_fisico_porc"] / 100

#     if x["monto_gastado"] == 0:
#         return (x["delta"] / x["delta_real"]) * (x["avance_fisico_porc"] / 100)

#     if x["monto_proyecto"] == 0:
#         return (x["delta"] / x["delta_real"]) * (x["avance_fisico_porc"] / 100)

#     if x["delta_real"] == 0:
#         return (x["monto_proyecto"] / x["monto_gastado"]) * (
#             x["avance_fisico_porc"] / 100
#         )

#     if x["delta"] == 0:
#         return (x["monto_proyecto"] / x["monto_gastado"]) * (
#             x["avance_fisico_porc"] / 100
#         )

#     return (
#         (x["delta"] / x["delta_real"])
#         * (x["monto_proyecto"] / x["monto_gastado"])
#         * (x["avance_fisico_porc"] / 100)
#     )


def f_anonima(x: pd.Series) -> float:
    monto_gastado = x["monto_gastado"]
    delta_real = x["delta_real"]
    avance_fisico_porc = x["avance_fisico_porc"]
    monto_proyecto = x["monto_proyecto"]
    delta = x["delta"]

    if monto_gastado == 0 and delta_real == 0:
        if delta > 30:
            return 0

        return avance_fisico_porc / 100

    if monto_gastado == 0:
        return (delta / delta_real) * (avance_fisico_porc / 100)

    if monto_proyecto == 0:
        return (delta / delta_real) * (avance_fisico_porc / 100)

    if delta_real == 0:
        return (monto_proyecto / monto_gastado) * (avance_fisico_porc / 100)

    if delta == 0:
        return (monto_proyecto / monto_gastado) * (avance_fisico_porc / 100)

    return (
        (delta / delta_real)
        * (monto_proyecto / monto_gastado)
        * (avance_fisico_porc / 100)
    )

import datetime
from datetime import date
from typing import Optional, Tuple, List, Dict, Any
from .prueba import category_entidad

import numpy as np
import pandas as pd

from re import A

from ..transformation.transform_data_utils import (
    validar_datos_utm2,
    transformar_utm_latlon,
    status_proyect,
    f_anonima,
)


class Transformer:
    def transform_all_data(
        self, data: Tuple[Dict, Dict, Dict, Dict]
    ) -> Tuple[pd.DataFrame]:
        pro = self.transform_proyect(data[0])
        mounts = self.transform_amounts(data[1], pro)
        accountability = self.transform_accountability(data[2])
        proyect, entity = self.transform_entity(data[3], df_psa=mounts[1], df_monto=mounts[0], dfs=accountability)

        return proyect, entity

    def transform_proyect(self, data: List[Dict]) -> pd.DataFrame:
        print("➡ proyectos :", "Iniciada la Transformacion")

        psa = []

        for p in data:
            p["montos_ids"] = p["montos_ids"][0]
            p["parroquia"] = p["parroquia_id"][1]
            p["municipio"] = p["municipio_id"][1]
            p["ciclo"] = p["ciclo_id"][1]

            p["entidad"] = p["partner_id"][1]
            p["tipo_entidad"] = (
                "Secretaría" if "Secretaría" in str(p["partner_id"]) else "Ente"
            )

            p["huso"] = int(p["huso_id"][1]) if p["huso_id"] else 0

            subcategoria = p["subcategoria_id"][1].split("/")

            p["sector"], p["categoria"], p["subcategoria"] = (
                subcategoria[0],
                subcategoria[1],
                subcategoria[2],
            )

            p["vertice_id"] = p.get("vertice_id", "xxx")[1]
            p["programa_id"] = p.get("programa_id", "xxx")[1]

            del (
                p["ciclo_id"],
                p["parroquia_id"],
                p["partner_id"],
                p["municipio_id"],
                p["subcategoria_id"],
                p["huso_id"],
            )

            psa.append(p)

        df_psa = pd.DataFrame(psa)
        df_psa = df_psa.query("fecha_inicio != '0202-01-09'")

        print("➡ proyectos :", "Finalizo la transformacion")
       
        return df_psa

    def transform_amounts(self, data: List[Dict], df_psa: pd.DataFrame) -> pd.DataFrame:
        print("➡ montos :", "Inicio la transformacion")

        df_monto = pd.DataFrame(data)
        df_monto.rename(columns={"id": "montos_ids"}, inplace=True)

        # ---------------------------------------------------

        l_drop: List[str] = ["montos_ids"]
        df_psa = df_psa.merge(df_monto, on="montos_ids")

        # ------------------------------------------------------

        df_psa = validar_datos_utm2(df_psa, "huso", "coord_este", "coord_norte")
        df_psa = transformar_utm_latlon(df_psa, "huso", "coord_este", "coord_norte")

        print("➡ montos :", "Finalizo la transformacion ")
        print(len(df_psa))
        print('=====================================')
        return df_monto , df_psa

    def transform_accountability(self, data:List[Dict]) -> pd.DataFrame:
        print("➡ rendicion:", "Inicio la transformacion")

    
        dfs = pd.DataFrame(data)

        dfs["monto"] = dfs["monto"].str[0]
        dfs.rename(columns={"monto": "id_monto"}, inplace=True)
        dfs["monto_gastado"] = (
            dfs["monto_gastado"]
            .str.split(":")
            .str[1]
            .str.replace(".", "")
            .str.replace(",", ".")
            .astype(float)
        )
        dfs["monto_gastado"].fillna(0, inplace=True)

        dfs["avance_financiero"] = (
            dfs["avance_financiero"]
            .str.split(":")
            .str[1]
            .str.replace(".", "")
            .str.replace(",", ".")
            .astype(float)
        )
        dfs["avance_financiero"].fillna(0, inplace=True)


        dfs["proyecto_id"] = dfs["proyecto_id"].str[1]
        dfs["entidad_id"] = dfs["entidad_id"].str[1]

        dfs["avance_fisico_porc"] = (
            dfs["avance_fisico_porc"].str.replace("%", "").astype(float)
        )
        dfs["avance_fisico_porc"].fillna(0, inplace=True)

        dfs["avance_fisico"] = dfs["avance_fisico"].str.replace("%", "").astype(float)
        dfs["avance_fisico"].fillna(0, inplace=True)

        dfs.rename(columns={"id": "id_rsa", "state": "estatus_rsa"}, inplace=True)
        print(len(dfs))
        print(dfs.head(5))
        print('=====================================')

        print("➡ rendicion:", "Finalizo la transformacion")
        return dfs

    
    def transform_entity(
        self,
        data: List[Dict],
        df_psa: pd.DataFrame,
        df_monto: pd.DataFrame,
        dfs: pd.DataFrame,
    ) -> Tuple[Dict, Dict]:
        print("➡ entidad:", "Inicio la transformacion")

        df_asa = pd.DataFrame(
            [
                {"respuesta": x["respuesta"], "id_rsa": x["rendicion_id"][0]}
                for x in data
                if x["pregunta_id"][0] == 24
            ]
        )

        df_asa["id_rsa"] = df_asa["id_rsa"].astype(int)

        df_asa.rename(columns={"respuesta": "fecha_culminacion"}, inplace=True)

        dfs = dfs.merge(df_asa, on="id_rsa", how="left")

        df_asa = None

        ###############################################################

        l_drop = ["montos_ids","monto_proyecto"]

        new = dfs.merge(df_monto, left_on="id_monto", right_on="montos_ids").drop(
            columns=l_drop
        )

        df_psa["fecha_inicio"] = pd.to_datetime(df_psa["fecha_inicio"])

        # print(df_psa.loc[df_psa['correlativo'] == "PA-2023-C-1-E-40-00000759" , ['fecha_inicio', 'correlativo']])
        # print(df_psa.query("fecha_inicio == '202-01-09 00:00:00'"))

        df_psa["rsa"] = df_psa.apply(
            lambda x: True
            if x["state"] in ["aprobado", "culminado"]
            and x["fecha_inicio"] < pd.Timestamp(date.today())
            else False,
            axis=1,
        )
        df_new = df_psa.merge(
            new, left_on="correlativo", right_on="proyecto_id", how="left"
        )

        df_new[["id_monto", "id_rsa"]] = df_new[["id_monto", "id_rsa"]].fillna(-1)
        df_new[["id_monto", "id_rsa"]] = df_new[["id_monto", "id_rsa"]].astype(int)
        df_new[["id_monto", "id_rsa"]] = df_new[["id_monto", "id_rsa"]].astype(str)

        df_new.loc[
            (df_new["rsa"] == True) & (df_new["id_rsa"] != "-1"), "rsa_category"
        ] = "Rindio"
        df_new.loc[
            (df_new["rsa"] == True) & (df_new["id_rsa"] == "-1"), "rsa_category"
        ] = "Por rendir"
        df_new.loc[df_new["rsa"] == False, "rsa_category"] = "No requiere"

        df_new.loc[(df_new["adjudicacion"] == False), "adjudicacion"] = "No aplica"
        df_new.loc[(df_new["state"] == "aprobado"), "adjudicacion"] = "Sin rendicion"

        df_new[["id_monto", "id_rsa"]] = df_new[["id_monto", "id_rsa"]].replace(
            "-1", np.nan
        )
        df_new["porcentaje_financiero"] = df_new.apply(
            lambda x: (x["avance_financiero"] / x["monto_proyecto"]) * 100
            if x["monto_proyecto"] > 10 and x["rsa_category"] == "Rindio"
            else 100.00,
            axis=1,
        )

        df_new["estatus_new"] = df_new.apply(status_proyect, axis=1)

        ccd = ["montos_ids", "proyecto_id"]
        df_u = df_new.drop(columns=ccd)

        df_new = None

        df_u["adjudicacion"].fillna("No aplica", inplace=True)

        # Dataframe de Projects

        df_projects = df_u.copy()
        print(category_entidad)
        df_projects=df_projects.merge(category_entidad, left_on='entidad', right_on='entidad', how="left")
        df_projects['state'] = df_projects['state'].str.capitalize()
        print(df_projects.columns)
        print('---------------------------------------------------------------------------')
        # print(df_projects.head(10))
        # print(df_projects['fecha_culminacion'])
        # Procesamiento Entidad

        df_u["fecha_fin"] = (
            pd.to_datetime(df_u["fecha_fin"])
            .apply(lambda x: x.date())
            .astype("datetime64[ns]")
        )
        df_u["fecha_inicio"] = (
            pd.to_datetime(df_u["fecha_inicio"])
            .apply(lambda x: x.date())
            .astype("datetime64[ns]")
        )

        df_u["delta"] = (df_u["fecha_fin"] - df_u["fecha_inicio"]).dt.days

        df_u_culminado = df_u.loc[~df_u.fecha_culminacion.isnull(),].copy()
        df_u_por_culminar = df_u.loc[df_u.fecha_culminacion.isnull(),].copy()

        df_u_por_culminar["delta_real"] = None
        df_u_por_culminar["eficiencia"] = None

        # -----------------------------------------------
        df_u_culminado["fecha_culminacion"] = (
            pd.to_datetime(df_u_culminado["fecha_culminacion"], format="%d-%m-%Y")
            .apply(lambda x: x.date())
            .astype("datetime64[ns]")
        )
        df_u_culminado["fecha_inicio_proyecto"] = (
            pd.to_datetime(df_u_culminado["fecha_inicio_proyecto"], format="%d-%m-%Y")
            .apply(lambda x: x.date())
            .astype("datetime64[ns]")
        )

        df_u_culminado["delta_real"] = (
            df_u_culminado["fecha_culminacion"]
            - df_u_culminado["fecha_inicio_proyecto"]
        ).dt.days

        df_u_culminado["eficiencia"] = df_u_culminado.apply(f_anonima, axis=1)

        df_u_culminado.loc[df_u_culminado["eficiencia"] > 2, "eficiencia"] = 2
        # -------------------------------------------

        df_u = pd.concat([df_u_culminado, df_u_por_culminar])

        # -----------------------------------------------
        df_u["conciderar"] = True

        df_u.loc[df_u.state.isin(["negado", "cancelado"]), "conciderar"] = False
        df_u.loc[
            (
                pd.to_datetime(df_u.fecha_fin, format="%Y-%m-%d")
                > datetime.datetime.now()
            ),
            "conciderar",
        ] = False

        # porque debieron de haber culminado
        df_u.loc[df_u["conciderar"] & df_u.state.isin(["aprobado"]), "eficiencia"] = 0

        df_u_culminado = None
        df_u_por_culminar = None
        # #----------------------------

        resumen_indicador_1 = (
            df_u.loc[
                df_u.conciderar, ["entidad_id", "eficiencia", "avance_fisico_porc"]
            ]
            .groupby("entidad_id", as_index=False)
            .mean()
        )

        resumen_indicador_2 = (
            df_u.loc[df_u.conciderar, ["entidad_id", "id", "state"]]
            .groupby(["entidad_id", "state"], as_index=False)
            .count()
            .pivot(index="entidad_id", columns="state", values="id")
            .fillna(0)
        )
        resumen_indicador_2 = resumen_indicador_2.reset_index()
        resumen_indicador_2["porcentaje_culminacion"] = (
            100
            * resumen_indicador_2["culminado"]
            / (resumen_indicador_2["aprobado"] + resumen_indicador_2["culminado"])
        )

        resumen_indicador = resumen_indicador_1.merge(
            resumen_indicador_2, on="entidad_id"
        )
        # resumen_indicador.drop(columns=['aprobado','culminado'], inplace=True)

        resumen_indicador.rename(
            columns={
                "eficiencia": "eficiencia_entidad",
                "avance_fisico_porc": "avance_fisico_porc_entidad",
                "porcentaje_culminacion": "porcentaje_culminacion_entidad",
            },
            inplace=True,
        )
        resumen_indicador.rename(
            columns={
                "entidad_id": "entidad",
                "porcentaje_culminacion_entidad": "porcentaje_culminados",
                "avance_fisico_porc_entidad": "porcentaje_avance_fisico",
                "eficiencia_entidad": "eficiencia",
                "culminado": "culminados",
            },
            inplace=True,
        )
        indicador = resumen_indicador[
            [
                "entidad",
                "porcentaje_culminados",
                "porcentaje_avance_fisico",
                "eficiencia",
                "aprobado",
                "culminados",
            ]
        ]

        indicador["id"] = indicador.index.tolist()
        print("➡ entidad :", "Finaliza la transformacion")
        print(len(indicador))
        print('=====================================')
        return df_projects.to_dict("records"), indicador.to_dict("records")

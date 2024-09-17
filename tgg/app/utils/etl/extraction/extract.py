import time
import pandas as pd

from functools import reduce
from typing import Optional, Tuple, List, Dict, Any

import odoorpc

from .odoo_connection import odoo_conn, get_data


class Extractor:
    def __init__(self):
        self.odoo_conn = odoo_conn()

    def extract_all_data(self) -> Tuple[odoorpc.ODOO]:
        proyects, ids_amount = self.extract_proyectos()
        mount = self.extract_monts(ids_amount)
        accountability = self.extact_accountability()
        entity = self.extract_entity()
        print(
            f"proyecto: {len(proyects)}, mount: {len(mount)}, accountability:{len(accountability)}, entity:{len(entity)}"
        )
        return proyects, mount, accountability, entity

    def extract_proyectos(self) -> Tuple[odoorpc.ODOO, List[int]]:
        print("➡ proyectos :", "Inicio de extraccion")
        model_proj = "jpv_cp.carga_proyecto"

        columns_project = [
            "correlativo",
            "nombre_proyecto",
            "descripcion_proyecto",
            "subcategoria_id",
            "montos_ids",
            "state",
            "municipio_id",
            "parroquia_id",
            "ciclo_id",
            "partner_id",
            "huso_id",
            "coord_norte",
            "coord_este",
            "fecha_inicio",
            "fecha_fin",
            "create_date",
            "write_date",
            "vertice_id",
            "programa_id",
        ]

        try:
            ps = get_data(model_proj, columns_project, self.odoo_conn)
        except Exception as e:
            print("Error al obtener la data:", e)
            raise Exception("Error al obtener la data") from e

        ids_amount = [x["montos_ids"][0] for x in ps]

        print("➡ proyectos :", "Finalizada la extraccion")
        time.sleep(0.7)
        return ps, ids_amount

    def extract_monts(self, ids_amount: List[int]) -> Optional[odoorpc.ODOO]:
        print("➡ montos :", "Inicio de extraccion")
        model_monto = "jpv_cp.monto_proyecto"

        columns_monto = ["id", "monto_proyecto"]

        try:
            data_monto: List[Dict[str, Any]] = self.odoo_conn.execute(
                model_monto, "read", ids_amount, columns_monto
            )
        except Exception as e:
            print("Error al obtener la data:", e)
            raise Exception("Error al obtener la data") from e

        print("➡ montos", "Finalizada la extracion ")
        time.sleep(4)
        return data_monto

    def extact_accountability(self) -> Optional[odoorpc.ODOO]:
        print("➡ rendicion :", "Inicio de extraccion")

        model = "jpv_rnd.rendicion"
        Rend = self.odoo_conn.env[model]
        rend_ids = Rend.search([])

        cols = [
            "entidad_id",
            "nombre_institucion",
            "proyecto_id",
            "estatus_proyecto",
            "state",
            "avance_fisico",
            "avance_fisico_porc",
            "avance_financiero",
            "inicio_administrativo",
            "tipo_ejecucion",
            "adjudicacion",
            "monto",
            "monto_gastado",
            "fecha_inicio_proyecto",
        ]
        try:
            aux = []
            for col in cols:
                coll=["id",col]
                
                rss = self.odoo_conn.execute(model, "read", rend_ids, coll)
                        
                aux.append([rss])


            dfs = [pd.DataFrame(d[0]) for d in aux]

            result = reduce(lambda left,right: pd.merge(left,right, on=['id']), dfs)
            #result = result.to_dict(orient='records')

            rs = result.to_dict(orient='records')

        except Exception as e:
            print("Error al obtener la data:", e)
            raise Exception("Error al obtener la data") from e

        print("➡ rendicion :", "Finalizada la extraccion")
        return rs

    def extract_entity(self) -> Optional[odoorpc.ODOO]:
        print("➡ entidad :", "Inicio de extraccion")
        model = "jpv_rnd.input_line"
        Avance = self.odoo_conn.env[model]
        avance_ids = Avance.search([])

        try:
            entity = self.odoo_conn.execute(
                model, "read", avance_ids, ["rendicion_id", "pregunta_id", "respuesta"]
            )

        except Exception as e:
            print("Error al obtener la data:", e)
            raise Exception("Error al obtener la data") from e

        print("➡ entidad :", "Finalizada la extraccion")
        time.sleep(0.7)
        return entity

from typing import Tuple, Dict
from ....models.V1 import Entida , Project
from app.core.V1.sessions import get_db


class Loader:

    def load_data(self, data: Tuple[Dict])-> None:
        self.save_proyect(data[0])
        self.save_entida(data[1])
        
    def save_entida(self,data: Dict)-> None:
        print("➡ Entidad :", "Iniciado el guardado")

        db = next(get_db())
        db.query(Entida).delete()
        db.commit()

        db = next(get_db())


        for i in data:
            
            entida = Entida(**i)
            db.add(entida)

            db.commit()
        print("➡ Entidad :", "Guardado finalizado")

    def save_proyect(self,data: Dict)-> None:
        print("➡ Proyectos :", "Iniciado el guardado")
            
        db = next(get_db())
        db.query(Project).delete()
        db.commit()

        db = next(get_db())
        
        for x in data:
                
            project = Project()
            project.correlativo = x["correlativo"]
            project.periodo_fiscal = x["correlativo"][3:7] if x["correlativo"] else '0'
            project.municipio = x["municipio"]
            project.parroquia = x["parroquia"]
            project.entidad = x["entidad"]
            project.tipo_entidad = x["tipo_entidad"]
            project.ciclo = x["ciclo"]
            project.nombre_proyecto = x["nombre_proyecto"]
            project.descripcion_proyecto = x["descripcion_proyecto"]
            project.state = x["state"]
            project.sector = x["sector"]
            project.categoria = x["categoria"]
            project.subcategoria = x["subcategoria"]
            project.monto_proyecto = x["monto_proyecto"]
            project.huso = x["huso"]
            project.coord_este = x["coord_este"]
            project.coord_norte = x["coord_norte"]
            project.datos_geograficos_validos = x["datos_geograficos_validos"]
            project.lat = x["lat"]
            project.lon = x["lon"]
            project.fecha_inicio = x["fecha_inicio"]
            project.fecha_fin = x["fecha_fin"]
            project.write_date = x["write_date"]
            project.create_date = x["create_date"]
            project.rsa_category = x["rsa_category"]
            project.avance_fisico_porc = x["avance_fisico_porc"]
            project.inicio_administrativo = x["inicio_administrativo"]
            project.entidad_id = x["entidad_id"]
            project.nombre_institucion = x["nombre_institucion"]
            project.monto_gastado = x["monto_gastado"]
            project.avance_fisico = x["avance_fisico"]
            project.avance_financiero = x["avance_financiero"]
            project.rsa = x["rsa"]
            project.id_rsa = x["id_rsa"]
            project.id_monto = x["id_monto"]
            project.tipo_ejecucion = x["tipo_ejecucion"]
            project.adjudicacion = x["adjudicacion"]
            project.porcentaje_financiero = x["porcentaje_financiero"]
            project.estatus_proyecto = x["estatus_proyecto"]
            project.estatus_rsa = x["estatus_rsa"]
            project.estatus_new = x["estatus_new"]
            project.fecha_inicio_proyecto=x["fecha_inicio_proyecto"]
            project.fecha_culminacion=x["fecha_culminacion"]
            project.vertice=x["vertice_id"]
            project.programa=x["programa_id"]
            project.category_entidad=x["category_entidad"]
            db.add(project)

            db.commit()
            
        print("➡ Proyecto :", "Guardado finalizado")



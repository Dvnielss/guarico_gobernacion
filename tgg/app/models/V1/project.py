import datetime

from sqlalchemy import Integer, String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.config.sql import Base


class Project(Base):
    __tablename__ = "projects"
    __table_args__ = {"schema": "gob"}

    id: Mapped[int] = mapped_column(primary_key=True)
    correlativo: Mapped[str] = mapped_column(String(30),nullable= True)
    periodo_fiscal:Mapped[str] = mapped_column(String(30),nullable= True)
    municipio: Mapped[str] = mapped_column(String(80),nullable= True)
    parroquia: Mapped[str] = mapped_column(String(80),nullable= True)
    entidad: Mapped[str] = mapped_column(String(200),nullable= True)
    tipo_entidad: Mapped[str] = mapped_column(String(80),nullable= True)
    ciclo: Mapped[str] = mapped_column(String(10),nullable= True)
    nombre_proyecto: Mapped[str] = mapped_column(String(600),nullable= True)
    descripcion_proyecto: Mapped[str] = mapped_column(nullable= True)
    state: Mapped[str] = mapped_column(String(100),nullable= True)
    sector: Mapped[str] = mapped_column(String(100),nullable= True)
    categoria: Mapped[str] = mapped_column(String(100),nullable= True)
    subcategoria: Mapped[str] = mapped_column(String(100),nullable= True)
    monto_proyecto: Mapped[float] = mapped_column(nullable= True)
    huso: Mapped[float] = mapped_column(nullable= True)
    coord_este: Mapped[float] = mapped_column(nullable= True)
    coord_norte: Mapped[float] = mapped_column(nullable= True)
    datos_geograficos_validos: Mapped[bool] = mapped_column(Boolean,nullable= True)
    lat: Mapped[float] = mapped_column(nullable= True)
    lon: Mapped[float] = mapped_column(nullable= True)
    write_date: Mapped[DateTime] = mapped_column(DateTime,nullable= True)
    create_date: Mapped[DateTime] = mapped_column(DateTime,nullable= True)
    fecha_inicio: Mapped[DateTime] = mapped_column(DateTime,nullable= True)
    fecha_fin: Mapped[DateTime] = mapped_column(DateTime,nullable= True)
    avance_fisico_porc: Mapped[float] = mapped_column(nullable= True)
    inicio_administrativo: Mapped[str] = mapped_column(String(100),nullable= True)
    entidad_id: Mapped[str] = mapped_column(String(600),nullable= True)
    nombre_institucion: Mapped[str] = mapped_column(String(600),nullable= True)
    monto_gastado: Mapped[float] = mapped_column(nullable= True)
    avance_fisico: Mapped[float] = mapped_column(nullable= True)
    avance_financiero: Mapped[float] = mapped_column(nullable= True)
    id_rsa: Mapped[str] = mapped_column(String(100),nullable= True)
    id_monto: Mapped[str] = mapped_column(String(100),nullable= True)
    rsa: Mapped[bool] = mapped_column(Boolean, default=False)
    rsa_category: Mapped[str] = mapped_column(String(100),nullable= True)
    tipo_ejecucion: Mapped[str] = mapped_column(String(100),nullable= True)
    adjudicacion: Mapped[str] = mapped_column(String(100),nullable= True)
    porcentaje_financiero: Mapped[float] = mapped_column(nullable= True)
    estatus_proyecto: Mapped[str] = mapped_column(String(100),nullable= True)
    estatus_rsa: Mapped[str] = mapped_column(String(100),nullable= True)
    estatus_new: Mapped[str] = mapped_column(String(100),nullable= True)
    fecha_inicio_proyecto: Mapped[str] = mapped_column(String(100),nullable= True)
    fecha_culminacion: Mapped[str] = mapped_column(String(100),nullable= True)
    vertice: Mapped[str] = mapped_column(String(600),nullable= True)
    programa: Mapped[str] = mapped_column(String(600),nullable= True)
    category_entidad: Mapped[str] = mapped_column(String(600),nullable= True)

    created_date: Mapped[DateTime] = mapped_column(
        DateTime, default=datetime.datetime.now
    )

class Entida(Base):
    __tablename__ = "entidada"
    __table_args__ = {"schema": "gob"}

    id: Mapped[int] = mapped_column(primary_key=True)
    entidad: Mapped[str] = mapped_column(String(200),nullable= True)
    porcentaje_culminados: Mapped[float] = mapped_column(nullable= True)
    porcentaje_avance_fisico: Mapped[float] = mapped_column(nullable= True)
    eficiencia: Mapped[float] = mapped_column(nullable= True)
    aprobado: Mapped[int] = mapped_column(Integer,nullable= True)
    culminados: Mapped[int] = mapped_column(Integer,nullable= True)

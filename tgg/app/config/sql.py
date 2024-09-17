from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.schemas.V1.config_scheme import settings_env




# Configuración del pool de conexiones
pool_size = settings_env.POOL_SIZE
max_overflow = settings_env.MAX_OVERFLOW
pool_timeout = settings_env.POLL_TIMEOUT
pool_recycle = settings_env.POOL_RECYCLE

# Crear el motor de la base de datos
engine = create_engine(
    settings_env.DATABASE_URL,
    pool_size=pool_size,
    max_overflow=max_overflow,
    pool_timeout=pool_timeout,
    pool_recycle=pool_recycle,
)


Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


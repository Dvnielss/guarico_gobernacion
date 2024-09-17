from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSettings(BaseSettings):
    DATABASE_URL: str = "postgresql://gestion_guarico:MepmD1VSbEIDB6ncJNzLjwFsk5UgVa@db:5432/DATABASE"

    POOL_SIZE: int = 20
    MAX_OVERFLOW: int = 15
    POLL_TIMEOUT: int = 60
    POOL_RECYCLE: int = 2400

    MAX_FAILED_LOGIN_ATTEMPTS: int = 5
    LOCK_DURATION_MINUTES: int = 5
    TIME_EXPIRATION_TOKEN_JWT: int = 30
    
    
    SECRET_KEY: str = "oidjfn0p9425[v'v2/45201\345.2'45203245]"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRES: int = 60
    
    
    # base de datos antigua de caracas
    #ODOO_HOST:str = "190.205.43.250"
    ODOO_HOST:str = "192.168.10.20" #"190.205.119.210" 
    ODOO_PORT:int = 8079
    ODOO_PROTOCOL :str = "jsonrpc"

    ODOO_DB:str = "GESTION"
    ODOO_USER:str = "pentaho"
    ODOO_PASS:str = "P3nt4j0.kq2t"
    
    # #base de datos nueva
    # ODOO_HOST:str = "201.249.189.185"
    # ODOO_PORT:int = 3828
    # ODOO_PROTOCOL :str = "jsonrpc"

    # ODOO_DB:str = "DB_GUARICO"
    # ODOO_USER:str = "pentaho"
    # ODOO_PASS:str = "P3nt4j0.kq2t"

    TOKEN_TELEGRAM_BOT:str = "5833334785:AAH1mxvSJIbunreXgmOc9ZvoLhstFEJWP8c"

    API_HOST: str = "0.0.0.0"
    API_PORT: int = 7501
    API_DEBUG: bool = True

    model_config = SettingsConfigDict(env_file=".env")


settings_env = EnvSettings()

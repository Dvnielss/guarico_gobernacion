# app/__init__.py

# Importar módulos desde el paquete app

from .core.V1 import sessions


from .routes.api.V1.update import update
from .routes.api.V1.cronjobs import cronjobs


from .routes.dashboard.auth import auth
from .routes.dashboard.dashboard import dashboard
from .routes.dashboard.users import user
from .routes.dashboard.cron import cron_t
from .routes.dashboard.bot import bot



from .schemas.V1 import config_scheme
from .config import  sql


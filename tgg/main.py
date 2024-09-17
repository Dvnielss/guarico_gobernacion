from fastapi import Depends, FastAPI, responses
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.core.V1.security import login_require_admin
from app.core.V1.sessions import get_db

from app.schemas.V1.config_scheme import settings_env
from app import update, cronjobs, auth, dashboard, user, cron_t,bot
from app.utils.cron_handler import start_cron

from starlette.middleware.sessions import SessionMiddleware

from app.seeders.seeders import seed_data


app = FastAPI(title="TGG", version="1.0.0", redoc_url=None)
templates = Jinja2Templates(directory="app/views/templates")
app.mount("/static", StaticFiles(directory="app/views/static"), name="static")

app.add_middleware(SessionMiddleware, secret_key="tu_clave_secreta")


@app.exception_handler(404)
async def custom_404_handler(request, __):
    return templates.TemplateResponse("errors/error_404.html", {"request": request})


@app.exception_handler(500)
async def custom_404_handler(request, __):
    return templates.TemplateResponse("errors/error_500.html", {"request": request})


@app.on_event("startup")
async def startup_event():
    start_cron()
    db = next(get_db())
    # db.execute("CREATE SCHEMA IF NOT EXISTS public")
    # db.execute("CREATE SCHEMA IF NOT EXISTS gob")

    seed_data(db)


@app.get("/", include_in_schema=False)
def refirect_docs():
    return responses.RedirectResponse("/singin")


app.include_router(update, prefix="/api/v1", tags=["Update"])
app.include_router(cronjobs, prefix="/api/v1", tags=["Cronjobs"])


app.include_router(auth)
app.include_router(dashboard)
app.include_router(cron_t)
app.include_router(user)
app.include_router(bot)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings_env.API_HOST,
        port=settings_env.API_PORT,
        log_level="info" if settings_env.API_DEBUG else "debug",
        reload=settings_env.API_DEBUG,
    )

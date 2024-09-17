from datetime import datetime
from sched import scheduler
from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session


from app.core.V1.security import login_require_admin
from app.models.V1 import Cron_update, Users_update, User
from app.utils.cron_handler import start_cron, status_cron, stop_cron, update_time_cron
from app.utils.env_update import update_env_odoo_conn
from ...core.V1.sessions import get_db


cron_t = APIRouter()
templates = Jinja2Templates(directory="app/views/templates")


@cron_t.get("/cron", response_class=HTMLResponse, include_in_schema=False)
def updating_cron(request: Request, user: User = Depends(login_require_admin)):
    flash_message = request.session.pop("flash_message", None)
    cron_status = status_cron()

    return templates.TemplateResponse(
        "/dashboard/config/cronjobs.html",
        {
            "request": request,
            "flash_message": flash_message,
            "user": user,
            "cron_status": cron_status,
        },
    )


@cron_t.post("/cron/activated", include_in_schema=False)
def activated_cron(request: Request, user: User = Depends(login_require_admin)):
    if start_cron():
        error_message = ["success", "El cron a sido activado"]
    else:
        error_message = ["danger", "Fallo la activacion del cron"]

    request.session["flash_message"] = {
        "category": error_message[0],
        "message": error_message[1],
    }
    return RedirectResponse("/cron", status_code=status.HTTP_303_SEE_OTHER)


@cron_t.post("/cron/deactivated", include_in_schema=False)
def desactivate_cron(request: Request, user: User = Depends(login_require_admin)):
    if stop_cron():
        error_message = ["info", "El cron a sido desactivado"]
    else:
        error_message = ["danger", "Fallo la activacion del cron"]

    request.session["flash_message"] = {
        "category": error_message[0],
        "message": error_message[1],
    }
    return RedirectResponse("/cron", status_code=status.HTTP_303_SEE_OTHER)


@cron_t.post("/cron/updating", include_in_schema=False)
async def updating_cron(request: Request, user: User = Depends(login_require_admin)):
    form_data = await request.form()
    time = form_data.get("time")
    if time:
        try:
            time = int(time)
            if 720 < time < 1440:
                if update_time_cron(int(time)):
                    error_message = [
                        "info",
                        f"Tiempo del cron Actualizado a {time} minutos",
                    ]
                else:
                    error_message = [
                        "warning",
                        "Fallo la actializacion puedes activar el cron o interlo mas tarde",
                    ]
            else:
                error_message = [
                    "danger",
                    "El tiempo de la actualizacion debe ser mayor a 720 minutos y menor a 1400 minutos",
                ]

        except ValueError:
            error_message = ["danger", "Debes introducir un tiempo valido"]

    else:
        error_message = ["warning", "Debes introducir un tiempo valido"]

    
    return RedirectResponse("/cron", status_code=status.HTTP_303_SEE_OTHER)

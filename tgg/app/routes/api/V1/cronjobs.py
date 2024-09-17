from fastapi import APIRouter, Depends, HTTPException

from app.core.V1.security import verify_credentials
from app.utils.cron_handler import start_cron, stop_cron, update_time_cron, status_cron


cronjobs = APIRouter()


@cronjobs.post("/cronjobs/start")
async def start_cronjob(credentials=Depends(verify_credentials)):
    if start_cron():
        return {"message": "El cron a sido activado"}

    return {"message": "Fallo al iniciar el cron puedes interlo mas tarde"}


@cronjobs.post("/cronjobs/stop")
async def stop_cronjob(credentials=Depends(verify_credentials)):
    if stop_cron():
        return {"message": "El cron desactivado"}

    return {
        "message": "Fallo al detener el cron puedes activar el cron o interlo mas tarde"
    }


@cronjobs.put("/cronjobs/time")
async def update_cronjob_time(new_time: int, credentials=Depends(verify_credentials)):
    if 720 < new_time < 1440:
        if update_time_cron(new_time):
            return {"message": "Tiempo de todos los cronjobs actualizado correctamente"}
        else:
            return {"message": "El cron no a sido encontrado o fallo su actualizacion"}

    else:
        return {
            "message": "El tiempo de la actualizacion debe ser mayor a 720 minutos y menor a 1400 minutos"
        }


@cronjobs.get("/cronjobs/status")
async def status(credentials=Depends(verify_credentials)):
    if status_cron():
        return {"message": "El cron esta activo"}

    return {"message": "El cron esta desactivado"}

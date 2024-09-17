from typing import Optional


from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException


from app.core.V1.security import verify_credentials
from app.core.V1.sessions import get_db
from app.utils.update_etl import ETLUpdate


update = APIRouter()

etl_update = ETLUpdate()


@update.get("/update")
async def update_route(background_tasks: BackgroundTasks, credentials=Depends(verify_credentials)):
    if etl_update.is_running:
        return {"message": "Ejecutando una actualizacion espere o intentelo mas tarde"}

    background_tasks.add_task(etl_update.perform_etl_cron)
    return {"message": "Actualizando ETL"}




from fastapi import HTTPException
from app.core.V1.sessions import get_db
from app.models.V1.users import Users_update
from app.models.V1.update import Cron_update
from app.models.V1 import  Error_report
from app.utils.etl.etl_odoo import ETL
from datetime import datetime

from ..utils.bot_message import telegram_message_error




class ETLUpdate:
    def __init__(self):
        self.is_running = False

        
        
    def perform_etl_cron(self) -> None:
        db = next(get_db())
        if self.is_running:
            return
        try:
            self.is_running = True
            for _ in range(5):
                try:
                    etl = ETL().run_etl()
                    success = Cron_update(success=True)
                    db.add(success)
                    db.commit()
                    date = datetime.now()
                    telegram_message_error(f"[TGG] Etl cron actualizado de forma exitosa a las \n {date.strftime('%H:%M:%S')} del {date.strftime('%d/%m/%Y')} :D...")
                    break
                except Exception as e:
                    db.rollback()
                    success = Cron_update(success=False)
                    bot_report = Error_report()
                    db.add_all([success,bot_report])
                    db.commit()
                    date = datetime.now()
                    telegram_message_error(f"[TGG] Acurrido un error al actualizar el etl a las \n {date.strftime('%H:%M:%S')} del {date.strftime('%d/%m/%Y')} :(...")
                    raise HTTPException(status_code=500)
        finally:
            self.is_running = False
        
        
    def perform_etl_user(self,user_id:int):
        db = next(get_db())
        if self.is_running:
            return
        try:
            self.is_running = True
            for _ in range(5):
                try:
                    etl = ETL().run_etl()
                    success = Users_update(users=user_id,success=True)
                    db.add(success)
                    db.commit()
                    date = datetime.now()
                    telegram_message_error(f"[TGG] Etl actualizado de forma exitosa a las \n {date.strftime('%H:%M:%S')} del {date.strftime('%d/%m/%Y')} :D...")
                    break
                except Exception as e:
                    db.rollback()
                    success = Users_update(users=user_id,success=False)
                    bot_report = Error_report()
                    db.add_all([success,bot_report])
                    db.commit()
                    date = datetime.now()
                    telegram_message_error(f"[TGG] Acurrido un error al actualizar el etl a las \n {date.strftime('%H:%M:%S')} del {date.strftime('%d/%m/%Y')} :( ...")
                    return HTTPException(status_code=500)
        finally:
            self.is_running = False
        
        
            
            

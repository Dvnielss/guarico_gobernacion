from typing import Optional
from apscheduler.schedulers.background import BackgroundScheduler

from app.utils.etl.etl_odoo import ETL

from app.routes.api.V1.update import etl_update

scheduler = BackgroundScheduler()


def start_cron():
    try:
        job = scheduler.add_job(etl_update.perform_etl_cron, "interval", minutes=720)
        scheduler.start()

        return True
    except Exception as e:
        print("➡ e :", e)
        return False


def stop_cron():
    try:
        # Detener el cronjob
        scheduler.shutdown()
        return True
    except Exception as e:
        print("➡ e :", e)
        return False


def update_time_cron(new_time: int):
    try:
        # Obtener todos los trabajos del planificador
        jobs = scheduler.get_jobs()
        if jobs:
            # Cambiar el tiempo de todos los cronjobs
            for job in jobs:
                job.reschedule(trigger="interval", minutes=new_time)
            return True
        else:
            return False
    except Exception as e:
        return False


def status_cron():
    try:
        if scheduler.get_jobs():
            return True
        return False
    except Exception as e:
        print("➡ e :", e)

        return False

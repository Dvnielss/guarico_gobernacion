from datetime import datetime
from sched import scheduler
from fastapi import APIRouter, Request, Depends, status,BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import extract
from sqlalchemy.orm import Session


from app.core.V1.security import login_require, login_require_admin
from app.models.V1 import Cron_update, Error_report, Users_update,User
from app.utils.cron_handler import start_cron, status_cron, stop_cron, update_time_cron
from app.utils.env_update import update_env_odoo_conn
from app.routes.api.V1.update import etl_update
from app.core.V1.sessions import get_db
from odoorpc import ODOO


dashboard = APIRouter()
templates = Jinja2Templates(directory="app/views/templates")


@dashboard.get("/dashboard", response_class=HTMLResponse, include_in_schema=False)
async def home(request: Request,db:Session = Depends(get_db),user: User=Depends(login_require)):
    context = {}
    year = datetime.now().year
    
    context["request"] = request
    context["user"] = user
    context["jobs"] = status_cron()
    context["cron_update"] = db.query(Cron_update).order_by(Cron_update.create_at.desc()).limit(5).all()
    context["users_update"] = db.query(User,Users_update).join(Users_update).order_by(Users_update.create_at.desc()).limit(5).all()
    context["donut_cron"] =  len(db.query(Cron_update).filter(extract("YEAR", Cron_update.create_at) == year).all())
    context["donut_user"] =  len(db.query(Users_update).filter(extract("YEAR", Users_update.create_at) == year).all())
    context["chart_cron"] = [ len(db.query(Cron_update).filter(extract("YEAR", Cron_update.create_at) == year,extract("MONTH",Cron_update.create_at) == i).all()) for i in range(1,13)]
    context["chart_user"] = [ len(db.query(Users_update).filter(extract("YEAR", Users_update.create_at) == year,extract("MONTH",Users_update.create_at) == i).all()) for i in range(1,13)]
    context["bot_total"] = len(db.query(Error_report).filter(extract("YEAR", Error_report.create_at) == year).all())
    context["bot_chart"] = [ len(db.query(Error_report).filter(extract("YEAR", Error_report.create_at) == year,extract("MONTH",Error_report.create_at) == i).all()) for i in range(1,13)]
    error_last_year = sum([ len(db.query(Error_report).filter(extract("YEAR", Error_report.create_at) == year -1 ,extract("MONTH",Error_report.create_at) == i).all()) for i in range(1,13)])
    
    if error_last_year != 0:
        context["percentage_change"] = f" { ((sum(context['bot_chart']) - error_last_year) / error_last_year) * 100 }.2f "
    else:
        context["percentage_change"] = 0
    

    
    return templates.TemplateResponse("dashboard/dashboard.html", context)


#####
@dashboard.get("/updating", response_class=HTMLResponse, include_in_schema=False)
@dashboard.post("/updating", response_class=HTMLResponse, include_in_schema=False)
async def updating(request: Request, background_tasks: BackgroundTasks,user: User=Depends(login_require_admin)):
    if request.method == "GET":
        flash_message = request.session.pop("flash_message", None)

        return templates.TemplateResponse("dashboard/updating.html", {"request": request,"flash_message": flash_message,"user":user})

    elif request.method == "POST":
        
        if not etl_update.is_running:
            background_tasks.add_task(lambda: etl_update.perform_etl_user(user.id))
            error_message= ["warning", "Ejecutando actualizacion"]
        else:
            error_message= ["danger", "Ejecutando una actualizacion espere o intentelo mas tarde"]            
        
        request.session["flash_message"] = {"category": error_message[0],"message": error_message[1],}
        return RedirectResponse("/updating", status_code=status.HTTP_303_SEE_OTHER)
    


@dashboard.get("/odoo_conection", response_class=HTMLResponse, include_in_schema=False)
@dashboard.post("/odoo_conection", response_class=HTMLResponse, include_in_schema=False)
async def odoo_conection(request: Request, user: User=Depends(login_require_admin)):
    if request.method == "GET":
        flash_message = request.session.pop("flash_message", None)

        return templates.TemplateResponse(
            "dashboard/config/odoo_connection.html",
            {"request": request, "flash_message": flash_message,"user": user},
        )
    elif request.method == "POST":
        error_message = None

        form_data = await request.form()
        host = form_data.get("host").strip()
        port = int(form_data.get("port"))
        protocol = form_data.get("protocol").strip()
        database = form_data.get("database").strip()
        user = form_data.get("username").strip()
        password = form_data.get("password").strip()

        if host and port and protocol and database and user and password:
            try:
                odoo = ODOO(host=host, port=port, protocol=protocol)
                odoo.login(database, user, password)

                tables = [
                    "jpv_cp.carga_proyecto",
                    "jpv_cp.monto_proyecto",
                    "jpv_rnd.rendicion",
                    "jpv_rnd.input_line",
                ]
                for table in tables:
                    if (
                        not odoo.env["ir.model"].search_count([("model", "=", table)])
                        > 0
                    ):
                        raise ValueError(f"La tabla '{table}' no existe en Odoo.")

                odoo.logout()

                update_env_odoo_conn(
                    host,
                    port,
                    protocol,
                    database,
                    user,
                    password,
                )
                error_message = ["success", "Conexión Exitosa a Odoo"]
            except Exception as e:
                error_message = ["danger", "Error de Conexión a Odoo", e]

        request.session["flash_message"] = {
            "category": error_message[0],
            "message": error_message[1],
        }

        return RedirectResponse(
            "/odoo_conection", status_code=status.HTTP_303_SEE_OTHER
        )


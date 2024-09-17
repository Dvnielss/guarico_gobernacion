from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.core.V1.security import login_require_admin
from ...core.V1.sessions import get_db
from ...models.V1 import Bot_report, User
from ...utils.bot_message import telegram_message


bot = APIRouter(prefix="/bot")
templates = Jinja2Templates(directory="app/views/templates")


@bot.get("/", response_class=HTMLResponse, include_in_schema=False)
async def users(request: Request, db: Session = Depends(get_db), user: User = Depends(login_require_admin)):
    users = db.query(Bot_report).all()
    flash_message = request.session.pop("flash_message", None)

    return templates.TemplateResponse(
        "dashboard/bot/users.html",
        {"request": request, "users": users,
            "flash_message": flash_message, "user": user},
    )


@bot.get("/register", response_class=HTMLResponse, include_in_schema=False)
@bot.post("/register", response_class=HTMLResponse, include_in_schema=False)
async def singup(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(login_require_admin),
):
    if request.method == "GET":
        flash_message = request.session.pop("flash_message", None)

        return templates.TemplateResponse("dashboard/bot/register.html", {"request": request, "flash_message": flash_message, "user": user})

    elif request.method == "POST":
        from_data = await request.form()
        id_telegram = from_data.get("id_telegram")

        error_message = None

        if not id_telegram:
            error_message = [
                "danger", "El id del usuario de telegram es obligatorio."]

        if id_telegram:

            response = telegram_message(
                id_telegram, "[TGG] Usuario del sistema TGG registrado correctamente :D")

            if response.status_code == 200:

                user = db.query(Bot_report).filter(
                    Bot_report.user_id == id_telegram).first()

                if user:
                    error_message = ["warning","El usuario ya está registrado."]

                else:
                    register = Bot_report(user_id=id_telegram)
                    db.add(register)
                    db.commit()
                    error_message = [
                        "success", "Usuario de telegram registrado correctamente"]
            else:
                error_message = [
                    "danger", "Su id de telegram es incorrecto por favor ingrese uno valido"]

        request.session["flash_message"] = {
            "category": error_message[0], "message": error_message[1]}
        return RedirectResponse("/bot", status_code=status.HTTP_303_SEE_OTHER)


@bot.post(
    "/delete/{user_id}", response_class=HTMLResponse, include_in_schema=False
)
async def users_delete(request: Request, user_id: int, db: Session = Depends(get_db), user: User = Depends(login_require_admin)):
    error_message = None

    try:
        user = db.query(Bot_report).filter(Bot_report.id == user_id).first()
        if not user:
            error_message = "El usuario que intentas eliminar no ha sido encontrado."

        else:
            db.delete(user)
            db.commit()
            error_message = "Usuario eliminado exitosamente."

    except Exception as e:
        print("➡ e :", e)
        db.rollback()
        error_message = "Ha ocurrido un error. No se pudo eliminar el usuario."

    request.session["flash_message"] = {
        "category": "danger" if error_message else "success",
        "message": error_message,
    }

    return RedirectResponse("/bot", status_code=status.HTTP_303_SEE_OTHER)
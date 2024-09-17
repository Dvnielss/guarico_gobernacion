from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session


from app.core.V1.security import encrypt_password, login_require_admin
from ...core.V1.sessions import get_db
from ...models.V1 import User

user = APIRouter()
templates = Jinja2Templates(directory="app/views/templates")


@user.get("/users", response_class=HTMLResponse, include_in_schema=False)
async def users(request: Request, db: Session = Depends(get_db),user: User=Depends(login_require_admin)):
    users = db.query(User).filter(User.status==True, User.id != user.id).all()
    flash_message = request.session.pop("flash_message", None)

    return templates.TemplateResponse(
        "dashboard/users/users.html",
        {"request": request, "users": users, "flash_message": flash_message,"user": user},
    )


@user.get("/users/edit/{user_id}", response_class=HTMLResponse, include_in_schema=False)
@user.post("/users/edit/{user_id}", include_in_schema=False)
async def users_edit(request: Request, user_id: int, db: Session = Depends(get_db),user: User=Depends(login_require_admin)):
    if request.method == "GET":
        user_edit = db.query(User).filter(User.id == user_id).first()
        if not user_edit:
            return RedirectResponse("/users", status_code=status.HTTP_303_SEE_OTHER)

        flash_message = request.session.pop("flash_message", None)
        return templates.TemplateResponse("dashboard/users/edit.html",{"request": request, "user_edit": user_edit, "flash_message": flash_message,"user": user},)

    elif request.method == "POST":
        error_message = None

        user = db.query(User).filter(User.id == user_id).first()

        form_data = await request.form()
        rol = form_data.get("rol")
        password = form_data.get("password")

        if user and rol in ["ADMIN", "GUEST"] and password:
            try:
                user.rol = rol
                user.password = encrypt_password(password)
                db.commit()

                error_message = ["success", "Usuario editado correctamente."]
                request.session["flash_message"] = {
                    "category": error_message[0],
                    "message": error_message[1],
                }
                return RedirectResponse("/users", status_code=status.HTTP_303_SEE_OTHER)

            except Exception as e:
                db.rollback()
                error_message = [
                    "danger",
                    "Ha ocurrido un error al editar los datos del usuario.",
                ]
                request.session["flash_message"] = {
                    "category": error_message[0],
                    "message": error_message[1],
                }
                return RedirectResponse("/users", status_code=status.HTTP_303_SEE_OTHER)

        else:
            error_message = [
                "danger",
                "El rol o la contraseña no están en el formato correcto.",
            ]
            request.session["flash_message"] = {
                "category": error_message[0],
                "message": error_message[1],
            }

        return RedirectResponse(
            f"/users/edit/{user_id}", status_code=status.HTTP_303_SEE_OTHER
        )


@user.post(
    "/users/delete/{user_id}", response_class=HTMLResponse, include_in_schema=False
)
async def users_delete(request: Request, user_id: int, db: Session = Depends(get_db),user: User=Depends(login_require_admin)):
    error_message = None

    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            error_message = "El usuario que intentas eliminar no ha sido encontrado."

        else:
            user.status = False
            db.add(user)
            db.commit()
            error_message = "Usuario eliminado exitosamente."

    except Exception as e:
        db.rollback()
        error_message = "Ha ocurrido un error. No se pudo eliminar el usuario."

    request.session["flash_message"] = {
        "category": "danger" if error_message else "success",
        "message": error_message,
    }

    return RedirectResponse("/users", status_code=status.HTTP_303_SEE_OTHER)

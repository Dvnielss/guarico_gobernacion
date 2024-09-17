from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.V1.security import (
    encrypt_password,
    login_require_admin,
    validate_password_regex,
    verify_password,
    create_token,
)
from ...core.V1.sessions import get_db
from ...models.V1 import User

auth = APIRouter()
templates = Jinja2Templates(directory="app/views/templates")


@auth.get("/singin", response_class=HTMLResponse, include_in_schema=False)
@auth.post("/singin", include_in_schema=False)
async def login(request: Request, db: Session = Depends(get_db)):
    if request.method == "GET":
        logged_in = request.session.get("session", None)
        if logged_in:
            return RedirectResponse("/dashboard", status_code=status.HTTP_303_SEE_OTHER)
        
        return templates.TemplateResponse("auth/singin.html", {"request": request})
    elif request.method == "POST":
        from_data = await request.form()
        username = from_data.get("username")
        password = from_data.get("password")

        error_message = None

        if not username or not password:
            error_message = "El nombre de usuario y la contraseña son obligatorios."
        else:
            user = db.query(User).filter(User.username == username).first()
            if user:
                verify = verify_password(password, user.password)

                if verify:
                    payload_content: dict = {
                        "sub": str(user.id),
                        "iss": "IMS",
                        "typ": "Internal",
                    }
                    token = create_token(payload_content)

                    request.session["session"] = token
                    return RedirectResponse(
                        "/dashboard", status_code=status.HTTP_303_SEE_OTHER
                    )

            error_message = "El usuario o contrseña son incorrectos"

        return templates.TemplateResponse(
            "auth/singin.html", {"request": request, "error": error_message}
        )


@auth.get("/singup", response_class=HTMLResponse, include_in_schema=False)
@auth.post("/singup", response_class=HTMLResponse, include_in_schema=False)
async def singup(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(login_require_admin),
):
    if request.method == "GET":
        flash_message = request.session.pop("flash_message", None)

        return templates.TemplateResponse("auth/singup.html", {"request": request,"flash_message": flash_message ,"user": user})

    elif request.method == "POST":
        from_data = await request.form()
        username = from_data.get("username")
        password = from_data.get("password")

        error_message = None
        success_message = None

        if not username or not password:
            error_message= ["danger", "El nombre de usuario y la contraseña son obligatorios."]
        
        elif not validate_password_regex(password):             
            error_message= ["danger", "La contraseña debe tener al menos 8 caracteres, incluyendo al menos 1 letra mayúscula, 1 letra minúscula y 1 carácter especial."]

        else:
            user = db.query(User).filter(User.username == username).first()
            print("➡ user :", user)

            if user:
                if user.status == True:
                    error_message= ["warning", "El usuario ya está registrado."]            

                elif user.status == False:
                    error_message= ["warning", "El usuario se encuentra desactivado."]            

                    
            else:
                register = User(username=username, password=encrypt_password(password))
                db.add(register)
                db.commit()
                error_message= ["success", "Usuario registrado exitosamente."]         

                
        request.session["flash_message"] = {"category": error_message[0],"message": error_message[1],}
        return RedirectResponse("/singup", status_code=status.HTTP_303_SEE_OTHER)
    


@auth.get("/logout", response_class=HTMLResponse, include_in_schema=False)
async def logout(request: Request):
    request.session.clear()

    return RedirectResponse("/singin", status_code=status.HTTP_303_SEE_OTHER)

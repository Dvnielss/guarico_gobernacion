from datetime import datetime, timedelta
from typing import Optional
import re


from fastapi import Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session


from app.core.V1.sessions import get_db
from app.models.V1 import User
from app.schemas.V1.config_scheme import settings_env
from app.schemas.V1.jwt_scheme import TokenPayload, TokenDecode
from app.utils.exceptions import exception_permit_denied


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

security = HTTPBasic()


# Encripta la contrasena
def encrypt_password(password: str) -> str:
    return pwd_context.hash(password)


# Verifica la contrasena
def verify_password(plane_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plane_password, hashed_password)


def validate_password_regex(password:str)->bool:
    
    pattern = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
    is_valid = re.match(pattern, password)
    return is_valid is not None


# Crea un nuevo token
def create_token(data: TokenPayload, time_expire: Optional[int] = 20) -> str:
    timestamp = datetime.utcnow()

    expires = timestamp + timedelta(minutes=time_expire)
    data.update({"iat": timestamp, "exp": expires})

    token_jwt = jwt.encode(data, settings_env.SECRET_KEY, settings_env.ALGORITHM)
    return token_jwt


# Decodifica el Token
def decode_token(token: str) -> Optional[dict]:
    try:
        # Decodificamos el token JWT y verificamos su firma
        decode_token: TokenDecode = jwt.decode(token, settings_env.SECRET_KEY, algorithms=[settings_env.ALGORITHM])
        return decode_token

    except JWTError as e:
        print("➡ Error al decodificar el token:", e)
        return None


def check_general_jwt(db:Session,data:str)-> User:
    
    try:
        
        token = decode_token(data)
        
        user_id = token["sub"]
        exp_token = token["exp"]
        
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, headers={"Location": "/logout"})

        if  exp_token is None:
            raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, headers={"Location": "/logout"})

        expiration_time = datetime.fromtimestamp(exp_token)
        current_time = datetime.now()

        if current_time > expiration_time:
            raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, headers={"Location": "/logout"})
        

        user = db.query(User).filter(User.id == user_id ).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, headers={"Location": "/logout"})
        
        if not user.status:
            raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, headers={"Location": "/logout"})
        return user 

    except:
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, headers={"Location": "/logout"})


def login_require(request: Request)->Optional[User]:
    db= next(get_db())
    session_data = request.session.get("session",None)
    if not session_data:
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, headers={"Location": "/singin"})

    try:
        user = check_general_jwt(db,session_data)
        return user
    
    except JWTError:
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, headers={"Location": "/logout"})



def login_require_admin(request: Request)->Optional[User]:
    db= next(get_db())
    session_data = request.session.get("session",None)
    if not session_data:
        
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, headers={"Location": "/singin"})

    try:
        user = check_general_jwt(db,session_data)

        if user.rol != "ADMIN":
            raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, headers={"Location": "/dashboard"})
        return user 

    except JWTError:
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, headers={"Location": "/logout"})


def verify_credentials(credentials: HTTPBasicCredentials = Depends(security))->Optional[HTTPException]:
    db = next(get_db())
    input_user_name = credentials.username
    input_password = credentials.password
    
    user = db.query(User).filter(User.username == input_user_name).first()
    
    if user is None or not verify_password(input_password, user.password) or user.rol != "ADMIN" or user.status == False:
        raise exception_permit_denied


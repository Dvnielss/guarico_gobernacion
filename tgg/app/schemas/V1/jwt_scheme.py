from pydantic import BaseModel


class TokenPayload(BaseModel):
    sub: str  # Identificador único del usuario (sujeto)
    iss: str  # Emisor del token (puede ser el nombre de tu aplicación)
    typ: str  # Esta nos dice que tipo de token es es decir si fue generada para apis externa o para uso interno de la api de validacion

class TokenDecode(BaseModel):
    sub: str  # Identificador único del usuario (sujeto)
    iss: str  # Emisor del token (puede ser el nombre de tu aplicación)
    typ: str  # Esta nos dice que tipo de token es decir si fue generada para apis o para uso interno de la del sistema
    iat: int  # Tiempo hora y fecha en la que se creo el token
    exp: int  # Tiempo de expiracion que tiene el token
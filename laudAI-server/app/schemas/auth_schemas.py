from pydantic import BaseModel, EmailStr, Field

class TokenProviderData(BaseModel):
    """
    Classe para tipar as informações que deseja-se
    utilizar ao decodificar o token do firebase.
    """
    uid: str = Field(alias="sub")
    email: EmailStr
    role: str = Field(default="")
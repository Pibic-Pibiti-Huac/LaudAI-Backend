import os
import firebase_admin
from firebase_admin import auth, credentials
from fastapi import (
    Depends, 
    HTTPException
)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.settings import settings
from app.schemas.auth_schemas import TokenProviderData

firebase_credentials_path = os.path.expanduser(settings.PATH_FIREBASE_CREDENTIALS)

cred = credentials.Certificate(firebase_credentials_path)
firebase_admin.initialize_app(cred)

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenProviderData:
    """
    Verifica validade de um token do tipo Bearer token.
    """
    token = credentials.credentials

    try:
        decoded_token = auth.verify_id_token(token)
        return TokenProviderData(**decoded_token)

    except Exception:
        raise HTTPException(
                status_code=401,
                detail="Token inválido."
        )


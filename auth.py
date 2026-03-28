from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
import requests
import config

security = HTTPBearer()

TENANT_ID = "3020aae9-3196-4f1e-b919-6561c2e2f688"
CLIENT_ID = "3735e031-4ef2-4c7c-b132-702efcfe6c04"
JWKS_URL = f"https://login.microsoftonline.com/{TENANT_ID}/discovery/v2.0/keys"

def get_jwks():
    return requests.get(JWKS_URL).json()

def require_edu_email(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> dict:
    token = credentials.credentials

    try:
        jwks = get_jwks()
        header = jwt.get_unverified_header(token)
        
        key = next((k for k in jwks["keys"] if k["kid"] == header["kid"]), None)
        if not key:
            raise HTTPException(status_code=401, detail="Invalid token key.")

        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience=CLIENT_ID,
        )

        email = payload.get("preferred_username") or payload.get("email", "")

        if not email.endswith(".edu"):
            raise HTTPException(
                status_code=403,
                detail=f"Students only. '{email}' is not a .edu address."
            )

        return {"email": email, "payload": payload}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token verification failed: {str(e)}")
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
import requests
from functools import lru_cache

security = HTTPBearer()

TENANT_ID = "3020aae9-3196-4f1e-b919-6561c2e2f688"
CLIENT_ID = "3735e031-4ef2-4c7c-b132-702efcfe6c04"
JWKS_URL = f"https://login.microsoftonline.com/{TENANT_ID}/discovery/v2.0/keys"

# --- THE FIX: Caching the keys ---
@lru_cache(maxsize=1)
def get_jwks():
    """Fetches Microsoft's public keys once and caches them in memory."""
    try:
        return requests.get(JWKS_URL).json()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch Microsoft JWKS.")

def require_edu_email(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> dict:
    """Verifies the JWT and strictly enforces a .edu email address."""
    token = credentials.credentials

    try:
        jwks = get_jwks()
        header = jwt.get_unverified_header(token)
        
        key = next((k for k in jwks["keys"] if k["kid"] == header["kid"]), None)
        if not key:
            # If the key isn't found, clear the cache and try fetching fresh keys
            get_jwks.cache_clear()
            jwks = get_jwks()
            key = next((k for k in jwks["keys"] if k["kid"] == header["kid"]), None)
            if not key:
                raise HTTPException(status_code=401, detail="Invalid token key signature.")

        # Verify the token payload
        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience=CLIENT_ID,
        )

        # Extract email and enforce the college demographic
        email = payload.get("preferred_username") or payload.get("email", "")

        if not email.endswith(".edu"):
            raise HTTPException(
                status_code=403,
                detail=f"Access Denied. '{email}' is not a valid university address."
            )

        return {"email": email, "payload": payload}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token verification failed: {str(e)}")
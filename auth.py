from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from datetime import datetime, timedelta

security = HTTPBearer()
SECRET_KEY = "indy-relay-hackathon-secret"  # Change this later!
ALGORITHM = "HS256"

def create_access_token(email: str) -> str:
    """Generates a custom JWT valid for 24 hours."""
    expire = datetime.utcnow() + timedelta(hours=24)
    return jwt.encode({"sub": email, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

def require_edu_email(credentials: HTTPAuthorizationCredentials = Security(security)) -> dict:
    """Verifies the token and enforces the .edu rule."""
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        
        if not email or not email.endswith(".edu"):
            raise HTTPException(status_code=403, detail="Students only. .edu email required.")
            
        return {"email": email}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")
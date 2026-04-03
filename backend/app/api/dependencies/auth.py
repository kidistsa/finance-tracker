from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from app.core.config import settings
from app.core.db import db_client

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get('sub')
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid authentication credentials',
                headers={'WWW-Authenticate': 'Bearer'},
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    
    return {
        'uid': email,
        'user_id': email,
        'email': email
    }


async def get_current_active_user(
    current_user = Depends(get_current_user)
):
    user = db_client.fetch_one('SELECT email, role, status FROM users WHERE email = ?', (current_user['email'],))
    if not user:
        raise HTTPException(status_code=401, detail='User not found')
    
    if user.get('status') != 'active':
        raise HTTPException(status_code=403, detail='Account is not active')
    
    return dict(user)


async def require_admin(current_user: dict = Depends(get_current_active_user)):
    if current_user.get('role') != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Admin access required'
        )
    return current_user

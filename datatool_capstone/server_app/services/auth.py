import os
from orjson import loads, dumps
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, status, Request, HTTPException
#from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)

from typing import Annotated
from server_app.services.passwordmaker import PasswordMaker


from pydantic import BaseModel, ValidationError
from server_app.sql_app.schemas import User
from server_app.sql_app.repo.users import select_users
from server_app.sql_app.repo.user_scopes import select_user_scopes
from server_app.sql_app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = os.environ['VT_SERVER_SECRET_KEY']
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 86400 # 24시간 = 60초 * 60분 * 24시 = 86400000

SCOPES = {
    # user feature
    'datatool': 'Can `upload` files, `download` files and `execute` jobs.',
    'deletedocu': 'Can delete file in own IP address range.',
    # admin feature
    'assignuserscope': 'Can assign scopes to users',
    'b-user'    : 'Can browse users.',
    'r-user'    : 'Can read user information.',
    'e-user'    : 'Can edit user information.',
    'a-user'    : 'Can add user accounts',
    'd-user'    : 'Can delete user accounts',
}

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes=SCOPES,
)

async def get_from_redis(request: Request, key: str):
    return await request.app.state.redis.get(key)


async def set_to_redis(request: Request, key: str, value: str, ex: int):
    return await request.app.state.redis.set(key, value, ex=ex)


async def delete_from_redis(request: Request, key: str):
    return await request.app.state.redis.delete(key)


async def get_current_user(
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(oauth2_scheme)],
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    '''
    Token으로 인증
    1. redis로 인증(exp체크)
    2. token decode로 하여 username을 DB에서 검색하여 인증
    '''

    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    CREDENTIALS_EXCEPTION = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

    temp = await get_from_redis(request, token)
    if not temp:
        raise CREDENTIALS_EXCEPTION

    try:
        payload = loads(temp)
        #payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise CREDENTIALS_EXCEPTION
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=email)
    except (JWTError, ValidationError):
        raise CREDENTIALS_EXCEPTION
    user = (await db.scalars(select_users({'email': email}))).first()
    if user is None:
        raise CREDENTIALS_EXCEPTION
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user




async def authenticate_user(db: AsyncSession, email: str, password: str):
    '''
    id/pw로 인증
    '''
    user = (await db.scalars(select_users({'email': email, 'deleted_at': None}))).first()
    if not user:
        return False
    if not PasswordMaker.verify(password, user.hashed_password):
        return False
    if not user.is_verified:
        return False
    return user


async def authenticate_scope(db: AsyncSession, userid: int, scopes: list=None):
    '''
    userid로 scope 가져오기
    '''
    where = {
        'userid': userid,
        'deleted_at': None, # deleted_at이 NULL인 것만
    }
    if scopes != None:
        where['scopes'] = scopes
    
    temp = (await db.scalars(select_user_scopes(where))).all()
    return [ t.scope for t in temp]


async def create_access_token(request: Request, user: User, scopes: str):
    expire = datetime.utcnow() + timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS)
    to_encode = {
        'sub': user.email,
        'exp': expire.timestamp(),
        'scopes': scopes,
    }
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    _bool = await set_to_redis(request, token, dumps(to_encode), ex=ACCESS_TOKEN_EXPIRE_SECONDS)
    if _bool:
        return token


async def revoke_access_token(token: Annotated[str, Depends(oauth2_scheme)], request: Request):
    return await delete_from_redis(request, token)



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []


class UserInDB(User):
    hashed_password: str





async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.is_verified == False:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


if __name__ == "__main__":
    pass
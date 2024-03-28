from time import time
from fastapi import Request, HTTPException, Security, BackgroundTasks
from server_app.services.auth import authenticate_user, authenticate_scope, get_current_active_user, create_access_token, revoke_access_token
from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from server_app.sql_app.schemas import User
from server_app.sql_app.database import get_db
from server_app.services.common import LoggingAPIRoute
from sqlalchemy.ext.asyncio import AsyncSession





class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None


router = APIRouter(tags=["auth"], route_class=LoggingAPIRoute)

@router.post("/token", response_model=Token)
async def login_for_access_token(
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization failed",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if form_data.scopes:
        # scope가 있으면 scope가 가능한지도 체크
        scopes = await authenticate_scope(db, user.id, form_data.scopes)
        if len(scopes) != len(form_data.scopes):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid scope",
                headers={"WWW-Authenticate": "Bearer"},
            )
    else:
        # scope가 없으면 모든 가능한 scope를 넣어줌
        scopes = await authenticate_scope(db, user.id)
        


    access_token = await create_access_token(request, user, scopes)

    #background_tasks.add_task(log_request, await request_to_logbody(request), None, user, 'Token accuired')

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/token/revoke")
async def revoke_for_access_token(current_user: Annotated[User, Depends(revoke_access_token)]):
    return {}


if __name__ == "__main__":
    pass
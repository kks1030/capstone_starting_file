import random
from datetime import datetime
from fastapi import Request, HTTPException, Security
from server_app.services.auth import get_current_active_user, SCOPES, oauth2_scheme
from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException
from pydantic import BaseModel
from server_app.sql_app.schemas import User, UserCreate
import server_app.sql_app.repo.users as user_repo
from server_app.sql_app.database import get_db
from server_app.services.common import LoggingAPIRoute
from sqlalchemy.ext.asyncio import AsyncSession
from server_app.sql_app.repo.user_scopes import select_user_scopes, upsert_user_scopes




class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None


router = APIRouter(tags=["users"], route_class=LoggingAPIRoute)


@router.get("/users/me", response_model=User)
async def read_me(
    current_user: Annotated[User, Security(get_current_active_user, scopes=[])]
):
    '''
    no scope 계정확인만 되면 가능
    '''
    return current_user


@router.patch("/users/me", response_model=User)
async def edit_me(
    request: Request,   # password 는 입력되지 않을 수도 있기 때문에, 에러를 방지하기 위해 request로 받는다.
    current_user: Annotated[User, Security(get_current_active_user, scopes=[])],
    db: AsyncSession = Depends(get_db)
):
    '''
    no scope 계정확인만 되면 가능
    '''
    values = await request.json()

    # 업데이트 하지 않을 값은 삭제한다.
    if 'id' in values:
        del values['id']
    if 'email' in values:
        del values['email']
    if 'is_verified' in values:
        del values['is_verified']

    # 있는 값만 업데이트하고, 없는 값은 그대로 둔다.
    if values['username'] == None:
        del values['username']
    if 'password' in values and not values['password']:
        del values['password']
    
    now = datetime.now()

    values['updated_by'] = current_user.id
    values['updated_at'] = now
    
    user = (await db.scalars(user_repo.update_user(values, {'id': current_user.id}))).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User update error")

    await db.commit()

    return user


@router.delete("/users/me", response_model=User)
async def delete_me(
    request: Request,
    current_user: Annotated[User, Depends(get_current_active_user)],
    token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncSession = Depends(get_db)
):
    '''
    (Soft) Delete user info
    '''
    now = datetime.now()
    hash = ''.join(chr(random.randrange(65,90)) for i in range(10))
    values = {
        'email': current_user.email + '_' + hash,
        'username': '삭제된 사용자 ' + hash,
        'deleted_at': now,
        'deleted_by': current_user.id
    }

    user = (await db.scalars(user_repo.update_user(values, {'id': current_user.id}))).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User update error")

    await db.commit()

    await request.app.state.redis.delete(token)

    return user



@router.get("/users/me/scope")
async def read_user_scope(
    current_user: Annotated[User, Security(get_current_active_user, scopes=[])],
    db: AsyncSession = Depends(get_db)
):
    user_scopes = (await db.scalars(select_user_scopes({'userid': current_user.id}))).all()

    res = [ {'scope': x.scope} for x in user_scopes if x.deleted_at == None ]
    
    return res


@router.get("/users", response_model=list[User])
async def browse_users(
    current_user: Annotated[User, Security(get_current_active_user, scopes=['b-user'])],
    search_keyword: str=None,
    is_verified: bool=None,
    page: int=0,
    db: AsyncSession = Depends(get_db)
):
    ITEM_CNT = 50
    where = {
        'offset': page * ITEM_CNT,
        'limit': ITEM_CNT,
    }

    if search_keyword != None:
        where['search_keyword'] = search_keyword
    if is_verified != None:
        where['is_verified'] = is_verified

    users = (await db.scalars(user_repo.select_users(where))).all()
    return users


@router.get("/users/{id}")
async def read_user(
    id: int,
    current_user: Annotated[User, Security(get_current_active_user, scopes=['r-user'])],
    db: AsyncSession = Depends(get_db)
):
    user = (await db.execute(user_repo.select_users_full({'id':id}))).mappings().first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if hasattr(user, 'hashed_password'):
        del user.hashed_password

    return user


@router.post("/users", response_model=User)
async def add_user(
    #request: Request,
    user: UserCreate,
    current_user: Annotated[User, Security(get_current_active_user, scopes=['a-user'])],
    db: AsyncSession = Depends(get_db)
):
    db_user = (await db.scalars(user_repo.select_users({'email': user.email}))).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    #value = await request.json()
    values = user.__dict__

    now = datetime.now()

    values['is_verified'] = False
    values['created_by'] = current_user.id
    values['created_at'] = now
    values['updated_by'] = current_user.id
    values['updated_at'] = now
    
    user = (await db.scalars(user_repo.insert_user(values))).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User insertion error")

    await db.commit()

    return user


@router.patch("/users/{id}", response_model=User)
async def edit_user(
    id: int,
    request: Request,   # password 는 입력되지 않을 수도 있기 때문에, 에러를 방지하기 위해 request로 받는다.
    current_user: Annotated[User, Security(get_current_active_user, scopes=['e-user'])],
    db: AsyncSession = Depends(get_db)
):
    db_user = (await db.scalars(user_repo.select_users({'id': id}))).first()
    if db_user == None:
        raise HTTPException(status_code=400, detail="User not found")
    
    values = await request.json()

    # 업데이트 하지 않을 값은 삭제한다.
    if 'id' in values:
        del values['id']
    if 'email' in values:
        del values['email']

    # 있는 값만 업데이트하고, 없는 값은 그대로 둔다.
    if values['username'] == None:
        del values['username']
    if 'password' in values and not values['password']:
        del values['password']
    if values['is_verified'] == None:
        del values['is_verified']

    now = datetime.now()

    values['updated_by'] = current_user.id
    values['updated_at'] = now
    
    user = (await db.scalars(user_repo.update_user(values, {'id': id}))).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User update error")

    await db.commit()

    return user


@router.delete("/users/{id}", response_model=User)
async def delete_user(
    id: int,
    request: Request,
    current_user: Annotated[User, Depends(get_current_active_user)],
    token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncSession = Depends(get_db)
):
    '''
    (Soft) Delete user info
    '''
    db_user = (await db.scalars(user_repo.select_users({'id': id}))).first()
    if db_user == None:
        raise HTTPException(status_code=400, detail="User not found")

    now = datetime.now()
    hash = ''.join(chr(random.randrange(65,90)) for i in range(10))
    values = {
        'email': db_user.email + '_' + hash,
        'username': '삭제된 사용자 ' + hash,
        'deleted_at': now,
        'deleted_by': current_user.id
    }

    user = (await db.scalars(user_repo.update_user(values, {'id': id}))).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User update error")

    await db.commit()

    return user


@router.get("/users/{id}/scope")
async def read_user_scope(
    id: int,
    current_user: Annotated[User, Security(get_current_active_user, scopes=['r-user'])],
    db: AsyncSession = Depends(get_db)
):
    user_scopes = (await db.scalars(select_user_scopes({'userid': id}))).all()

    res = [ {'scope': x.scope} for x in user_scopes if x.deleted_at == None ]
    
    return res


@router.put("/users/{id}/scope")
async def read_user_scope(
    id: int,
    request: Request,
    current_user: Annotated[User, Security(get_current_active_user, scopes=['assignuserscope'])],
    db: AsyncSession = Depends(get_db)
):
    params = await request.json()

    now = datetime.now()

    values_list1 = []
    values_list2 = []
    for k in SCOPES.keys():
        if params[k] == True:
            values_list1.append({'userid': id, 'scope': k, 'created_at': now, 'created_by': current_user.id, 'updated_at': now, 'updated_by': current_user.id, 'deleted_at': None, 'deleted_by': None})
        else:
            values_list2.append({'userid': id, 'scope': k, 'created_at': now, 'created_by': current_user.id, 'deleted_at': now, 'deleted_by': current_user.id})

    if 0 < len(values_list1):
        await db.execute(upsert_user_scopes(values_list1))
    if 0 < len(values_list2):
        await db.execute(upsert_user_scopes(values_list2))
    
    await db.commit()

    return {
        'message': 'User Scope 저장완료'
    }


if __name__ == "__main__":
    pass
from server_app.sql_app.models import User
from sqlalchemy import select, insert, update
from sqlalchemy.orm import aliased
from server_app.services.passwordmaker import PasswordMaker


def select_users(where: dict):
    q = select(User)
    
    if 'id' in where:
        q = q.where(User.id == where['id'])
    if 'email' in where:
        q = q.where(User.email == where['email'])
    if 'username' in where:
        q = q.where(User.username == where['username'])
    if 'is_verified' in where:
        q = q.where(User.is_verified == where['is_verified'])
    if 'deleted_at' in where:
        q = q.where(User.deleted_at == where['deleted_at'])

    if 'offset' in where:
        q = q.offset(where['offset'])
    if 'limit' in where:
        q = q.limit(where['limit'])

    if 'search_keyword' in where and where['search_keyword'] != None:
        q = q.where((User.username.like(f'%{where["search_keyword"]}%')) | (User.email.like(f'%{where["search_keyword"]}%')))

    return q


def select_users_full(where: dict):
    created_user = aliased(User, name='user1')
    updated_user = aliased(User, name='user2')
    deleted_user = aliased(User, name='user3')
    q = select(
        User.id,
        User.email,
        User.username,
        User.is_verified,
        User.created_at,
        created_user.username.label('created_by_username'),
        User.updated_at,
        updated_user.username.label('updated_by_username'),
        User.deleted_at,
        deleted_user.username.label('deleted_by_username')
    )
    q = q.select_from(User)
    q = q.join(created_user, created_user.id == User.created_by)
    q = q.join(updated_user, updated_user.id == User.updated_by)
    q = q.join(deleted_user, deleted_user.id == User.deleted_by, isouter=True)
    
    if 'id' in where:
        q = q.where(User.id == where['id'])
    if 'email' in where:
        q = q.where(User.email == where['email'])
    if 'username' in where:
        q = q.where(User.username == where['username'])
    if 'is_verified' in where:
        q = q.where(User.is_verified == where['is_verified'])
    if 'deleted_at' in where:
        q = q.where(User.deleted_at == where['deleted_at'])

    if 'offset' in where:
        q = q.offset(where['offset'])
    if 'limit' in where:
        q = q.limit(where['limit'])

    if 'search_keyword' in where and where['search_keyword'] != None:
        q = q.where((User.username.like(f'%{where["search_keyword"]}%')) | (User.email.like(f'%{where["search_keyword"]}%')))

    return q


def insert_user(values: dict):
    if 'password' in values:
        values['hashed_password'] = PasswordMaker.get_password_hash(values['password'])
        del values['password']
    
    q = insert(User).values(values).returning(User)
    return q


def update_user(values: dict, where: dict):
    if 'password' in values:
        values['hashed_password'] = PasswordMaker.get_password_hash(values['password'])
        del values['password']

    q = update(User)
    
    if 'id' in where:
        q = q.where(User.id == where['id'])
    if 'email' in where:
        q = q.where(User.email == where['email'])
    if 'username' in where:
        q = q.where(User.username == where['username'])
    if 'is_verified' in where:
        q = q.where(User.is_verified == where['is_verified'])

    q = q.values(values).returning(User)
    return q
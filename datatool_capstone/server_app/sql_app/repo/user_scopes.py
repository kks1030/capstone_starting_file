from server_app.sql_app.models import UserScope
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as upsert   # for upsert


def select_user_scopes(where: dict):
    q = select(UserScope)

    if 'id' in where:
        q = q.where(UserScope.id == where['id'])
    if 'userid' in where:
        q = q.where(UserScope.userid == where['userid'])
    if 'scopes' in where:
        q = q.where(UserScope.scope.in_(where['scopes']))
    if 'deleted_at' in where:
        q = q.where(UserScope.deleted_at == where['deleted_at'])

    return q

def upsert_user_scopes(values_list: list[dict]):
    '''
    values_list의 모든 columns은 동일하게 들어가 있어야한다.
    안그럼 set_에서 에러남
    >>> from sqlalchemy.dialects.sqlite import insert as sqlite_upsert
    >>> stmt = sqlite_upsert(User).values(
    ...     [
    ...         {"name": "spongebob", "fullname": "Spongebob Squarepants"},
    ...         {"name": "sandy", "fullname": "Sandy Cheeks"},
    ...         {"name": "patrick", "fullname": "Patrick Star"},
    ...         {"name": "squidward", "fullname": "Squidward Tentacles"},
    ...         {"name": "ehkrabs", "fullname": "Eugene H. Krabs"},
    ...     ]
    ... )
    >>> stmt = stmt.on_conflict_do_update(
    ...     index_elements=[User.name], set_=dict(fullname=stmt.excluded.fullname)
    ... )
    >>> session.execute(stmt)

    '''
    q = upsert(UserScope).values(values_list)

    to_update = {col: getattr(q.excluded, col) for col in values_list[0]}

    # update할때 아래 것들은 제외한다.
    del to_update['userid']
    del to_update['scope']
    del to_update['created_at']
    del to_update['created_by']

    q = q.on_conflict_do_update(
        index_elements=[UserScope.userid, UserScope.scope],
        #set_=dict(updated_at=q.excluded.updated_at, updated_by=q.excluded.updated_by, deleted_at=q.excluded.deleted_at, deleted_by=q.excluded.deleted_by)
        set_=to_update,
    )

    return q


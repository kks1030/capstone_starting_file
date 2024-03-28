from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Index, TIMESTAMP
from sqlalchemy.orm import relationship

from server_app.sql_app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_verified = Column(Boolean, default=False)
    created_by = Column(Integer)
    created_at = Column(TIMESTAMP)
    updated_by = Column(Integer)
    updated_at = Column(TIMESTAMP)
    deleted_by = Column(Integer)
    deleted_at = Column(TIMESTAMP)


class UserScope(Base):
    __tablename__ = "user_scopes"

    id = Column(Integer, primary_key=True, index=True)
    userid = Column(Integer, index=True, nullable=False)
    scope = Column(String, nullable=False)
    created_by = Column(Integer)
    created_at = Column(TIMESTAMP)
    updated_by = Column(Integer)
    updated_at = Column(TIMESTAMP)
    deleted_by = Column(Integer)
    deleted_at = Column(TIMESTAMP)


Index("scopes_idx_01", UserScope.userid, UserScope.scope)


if __name__ == '__main__':
    # 위에 정의된 모델들을 CREATE TABLE로 표시해준다. INDEX는 표시 안해준다. 걍 손으로 만드는 게 나은 듯...
    from sqlalchemy.schema import CreateTable
    from sqlalchemy.dialects import postgresql
    for table in Base.metadata.tables.values():
        print(CreateTable(table).compile(dialect=postgresql.dialect()))
    for index in Base.metadata.index.values():
        print(index)
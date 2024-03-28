CREATE USER datatool_capstone WITH PASSWORD 'datatool_capstone7720A123b456!!';

CREATE SCHEMA AUTHORIZATION datatool_capstone;

CREATE SEQUENCE datatool_capstone.users_seq;

CREATE TABLE datatool_capstone.users (
    id integer primary key DEFAULT nextval('datatool_capstone.users_seq'),
    email character varying(50) NOT NULL,
    username character varying(50) NOT NULL,
    hashed_password character varying(255) NOT NULL,
    is_verified bool default 'False',
    created_at timestamp,
    created_by integer,
    updated_at timestamp,
    updated_by integer,
    deleted_at timestamp,
    deleted_by integer
);

CREATE UNIQUE INDEX IF NOT EXISTS users_unq00 ON datatool_capstone.users( email );
CREATE        INDEX IF NOT EXISTS users_idx00 ON datatool_capstone.users( username );

CREATE SEQUENCE datatool_capstone.user_scopes_seq;

CREATE TABLE datatool_capstone.user_scopes (
    id      integer primary key DEFAULT nextval('datatool_capstone.user_scopes_seq'),
    userid  integer NOT NULL, 
    scope   character varying(50) NOT NULL,
    created_at timestamp,
    created_by integer,
    updated_at timestamp,
    updated_by integer,
    deleted_at timestamp,
    deleted_by integer
);

CREATE        INDEX IF NOT EXISTS user_scopes_idx00 ON datatool_capstone.user_scopes( userid );
CREATE UNIQUE INDEX IF NOT EXISTS user_scopes_unq00 ON datatool_capstone.user_scopes( userid, scope );


GRANT CONNECT ON DATABASE docuparser TO datatool_capstone;
GRANT USAGE ON SCHEMA datatool_capstone TO datatool_capstone;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA datatool_capstone TO datatool_capstone;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA datatool_capstone TO datatool_capstone;


-- passwordmaker.py에서 비밀번호를 생성해서 업데이트 하시기 바랍니다.
INSERT into datatool_capstone.users(email, username, hashed_password, is_verified, created_at, created_by, updated_at, updated_by)
values ('voctree@voctree.com', 'voctree', '$2b$12$5sMLF7GAoWC6hy9a1c3zfunYXp3EFQShKTshTq7BRCpdD28cdnGFm', true, now(), 1, now(), 1) -- datatool_capstone0322#%!

INSERT into datatool_capstone.users(email, username, hashed_password, is_verified, created_at, created_by, updated_at, updated_by)
values ('guest@voctree.com', 'guest', '$2b$12$js106qmLDsdNbv/UzDl6Hep.kt.cl6N/qT5nYJLh.TRIeHbbsKTDu', true, now(), 1, now(), 1) -- guestguestguestguestguestguest#%!

-- 기능설명은 server_app/README.md 참조
INSERT INTO datatool_capstone.user_scopes (userid, "scope", created_at, created_by, updated_at, updated_by) VALUES
(1, 'datatool'  , now(), 1, now(), 1),
(1, 'deletedocu', now(), 1, now(), 1),
(1, 'assignuserscope', now(), 1, now(), 1),
(1, 'b-user'    , now(), 1, now(), 1),
(1, 'r-user'    , now(), 1, now(), 1),
(1, 'e-user'    , now(), 1, now(), 1),
(1, 'a-user'    , now(), 1, now(), 1),
(1, 'd-user'    , now(), 1, now(), 1);

INSERT INTO datatool_capstone.user_scopes (userid, "scope", created_at, created_by, updated_at, updated_by) VALUES
(2, 'datatool'  , now(), 1, now(), 1),
(2, 'deletedocu', now(), 1, now(), 1);

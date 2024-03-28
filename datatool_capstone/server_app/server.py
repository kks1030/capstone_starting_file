'''
몇가지 기능을 Online API 로 서비스한다.

uvicorn server:app --port 80 --reload
uvicorn server:app --host 0.0.0.0 --port 80 --workers 4


메뉴얼: http://localhost/docs



'''
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.responses import ORJSONResponse
#from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import server_app.routers.auth as auth
import server_app.routers.common as common
import server_app.routers.users as users
from server_app.services.redis import get_redis
from server_app.services.common import error, LoggingAPIRoute





@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the redis connection
    app.state.redis = await get_redis()
    try:
        yield
    finally:
        # close redis connection and release the resources
        await app.state.redis.aclose()


app = FastAPI(default_response_class=ORJSONResponse, lifespan=lifespan)
app.include_router(auth.router)
app.include_router(common.router)
app.include_router(users.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",
        "https://*.voctree.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#app.mount("/static", StaticFiles(directory="resources/static"), name="static")

@app.exception_handler(HTTPException)
async def handle_unexpected_error(request, ex):
    await error(request, ex.detail, ex)
    res_body = {
        "detail": ex.detail
    }
    try:
        await LoggingAPIRoute._assign_x_request_id(request)
        res_body['X-Request-ID'] = request.state.x_request_id
    except:
        pass
    
    return ORJSONResponse(res_body, status_code=ex.status_code)

@app.exception_handler(Exception)
async def handle_unexpected_error(request, ex):
    ex1 = ex
    if hasattr(ex, 'orig') and ex.orig:
        ex1 = ex.orig

    print(ex1)
    if 0 < len(ex.args):
        # pgsql error
        await error(request, ex1.args[0], ex1)
    elif hasattr(ex1, 'detail'):
        await error(request, ex1.detail, ex1)
    else:
        await error(request, '', ex1)
    
    # Return a user-friendly error response
    return ORJSONResponse(
        {"detail": "An unexpected error occurred. Please try again later."},
        status_code=500
    )


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/health")
def read_root():
    return 1







if __name__ == "__main__":
    # 디버그 할때만 실행, 단독 실행은 아래 명령 입력
    # uvicorn server:app --port 80 --reload
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8086)
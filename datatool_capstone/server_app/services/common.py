import time
import uuid
import traceback
from typing import Any, Callable, Dict
from fastapi import Request
from fastapi.routing import APIRoute
from starlette.requests import Request
from starlette.responses import Response
from server_app.routers.auth import User


class LoggingAPIRoute(APIRoute):

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            await self._request_log(request)
            response: Response = await original_route_handler(request)
            await self._response_log(request, response)
            return response

        return custom_route_handler

    async def _request_log(self, request: Request) -> None:
        try:
            request.state.started_at = time.time()

            await LoggingAPIRoute._assign_x_request_id(request)

            message = 'START'
            if request.method in ("POST", "PUT", "PATCH"):
                if "application/json" in request.headers.get("content-type"):
                    message = f'START {await request.json()}'
                elif "form" in request.headers.get("content-type"):
                    message = f'START {await request.form()}'

            await info(request, message)
        except:
            print('error while request logging')

    @staticmethod
    async def _assign_x_request_id(request: Request):
        if hasattr(request.state, 'x_request_id'):
            return

        if 'x_request_id' in request.headers:
            request.state.x_request_id = request.headers.get('x_request_id')
        else:
            request.state.x_request_id = str(uuid.uuid4())


    @staticmethod
    async def _response_log(request: Request, response: Response) -> None:
        try:
            log_body = await request_to_logbody(request)

            log_body['taken_time'] = time.time() - request.state.started_at

            await info(request, 'END')
        except:
            print('error while response logging')


async def request_to_logbody(request: Request):
    '''
    request.json() 실행시 `stream consumed` 에러가 발생하게 하지 않기 위해서 미리 request 로 log body를 만들자.
    근데 막상 .json()을 안쓰게 됨 
    
    x-request-id 자동생성
    '''
    await LoggingAPIRoute._assign_x_request_id(request)

    log_body: dict[str, str] = {
        '@timestamp': time.time(),
        'ip': request.client.host,
        'method': request.method,
        'url': request.url.path,
        'query_params': str(request.query_params),
        #'headers': request.headers,
        'referer': request.headers.get('Referer'),
        'locale': request.headers.get('Locale'),
        'user_agent': request.headers.get('User-Agent'),
        'x_request_id': request.state.x_request_id
    }
    

    return log_body


async def error(request: Request, message: str, ex: Exception = None):
    log_body = await request_to_logbody(request)
    log_body['severity'] = 'ERROR'
    log_body['message'] = message
    log_body['traceback'] = ''.join(traceback.TracebackException.from_exception(ex).format())
    return print([log_body])


async def info(request: Request, message: str):
    '''
    Opensearch에 log를 전송 loglevel == INFO
    '''
    log_body = await request_to_logbody(request)
    log_body['severity'] = 'INFO'
    log_body['message'] = message
    return print([log_body])
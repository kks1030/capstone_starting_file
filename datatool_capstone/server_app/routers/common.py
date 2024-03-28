import os
import glob
import yaml
import shutil
from typing import List, Annotated
from pathlib import Path
from fastapi import Request, UploadFile, APIRouter, Security, BackgroundTasks
from datetime import datetime
from starlette.responses import FileResponse
from server_app.utils.mp_sync_logging import Logger
from server_app.utils.common_functions import get_1_depth_sub_path_n_file_list_by_extensions, unzip
from server_app.routers.auth import User, get_current_active_user
from server_app.services.common import LoggingAPIRoute


from sys import platform
if platform == "linux" or platform == "linux2":
    TMP_PATH = r'/tmp/datatool_capstone'
elif platform == "darwin":
    TMP_PATH = r'/tmp/datatool_capstone'
elif platform == "win32":
    TMP_PATH = r'/tmp/datatool_capstone'


router = APIRouter(tags=['common'], route_class=LoggingAPIRoute)

#templates = Jinja2Templates(directory="resources/view")


async def set_meta_start(workplace_dir: str, meta: dict, task: str, params: dict):
    '''
    시작한 작업을 history에 저장한다.
    '''
    history_item = {
        'task': task,
        'params': params,
        'start_at': datetime.now().timestamp(),
        'end_at': None,
        'status': 'Running',
    }
    meta['history'].append(history_item)

    await set_meta(os.path.join(workplace_dir, meta['dir_path'] + '.yml'), meta)


async def set_meta_end(workplace_dir: str, meta: dict, task: str, result_file: str, result_folder: str):
    '''
    종료한 작업을 history에 저장한다.
    '''
    meta['history'][-1]['end_at'] = datetime.now().timestamp()
    meta['history'][-1]['result_file'] = os.path.basename(result_file)
    meta['history'][-1]['result_folder'] = os.path.basename(result_folder)
    meta['history'][-1]['status'] = 'Success'

    await set_meta(os.path.join(workplace_dir, meta['dir_path'] + '.yml'), meta)


async def set_meta_error(workplace_dir: str, meta: dict, task: str, trg_dir: str, msg: str):
    '''
    에러난 작업을 history에 저장한다.
    '''
    meta['history'][-1]['end_at'] = datetime.now().timestamp()
    meta['history'][-1]['trg_dir'] = os.path.split(trg_dir)
    meta['history'][-1]['status'] = 'Error'
    meta['history'][-1]['msg'] = msg

    await set_meta(os.path.join(workplace_dir, meta['dir_path'] + '.yml'), meta)


async def set_meta(file_path: str, meta: dict):
    with Path(file_path).open('w', encoding='UTF-8') as f:
        yaml.dump(meta, f, allow_unicode=True)


async def get_meta(timestamp: str, request: Request):
    '''
    로깅 설정도 여기해줌
    '''
    private_dir = os.path.join(TMP_PATH, request.client.host)
    workplace_dir = os.path.join(private_dir, timestamp)
    
    # init Logger
    Logger(os.path.join(workplace_dir, 'server.log'))

    for yml_path in glob.glob(os.path.join(workplace_dir, "*.yml")):
        with Path(yml_path).open('r', encoding='UTF-8') as f:
            meta = yaml.load(f, Loader=yaml.FullLoader)

        return private_dir, workplace_dir, meta


@router.get("/main/request/{timestamp}/meta")
async def get_meta(timestamp: str, request: Request):
    '''
    조작 화면 initial 데이터
    '''
    private_dir, workplace_dir, meta = await get_meta(timestamp, request)

    return {
        'meta': meta,
    }


@router.post("/upload/file")
async def post_upload_file(
    files: List[UploadFile],
    request: Request,
    current_user: Annotated[User, Security(get_current_active_user, scopes=['datatool'])],
):
    '''
    일단 업로드를 받고
    1. 업로드 받은 파일의 tmp에 저장
    2. id를 발급하여 반환한다. 향후 이 id로 무엇을 할지 요청받는다.
    '''
    now_timestamp = str(datetime.now().timestamp())
    private_dir = os.path.join(TMP_PATH, request.client.host)
    workplace_dir = os.path.join(private_dir, now_timestamp)
    for file in files:
        sub_path, ext = os.path.splitext(file.filename)
        dir_path = os.path.join(workplace_dir, sub_path)
        file_path = os.path.join(dir_path, file.filename)
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        with Path(file_path).open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        if ext == '.zip':
            unzip(file_path, dir_path)
            os.remove(file_path)
            

        await file.close()

        # create meta file
        meta_path = os.path.join(workplace_dir, dir_path + '.yml')
        await set_meta(meta_path, {
            'uploader': current_user.email,
            'filename': file.filename,
            'dir_path': dir_path,
            'history': [],
        })

    return {
        'timestamp': now_timestamp
    }


@router.get('/parse/request/list')
async def get_parse_file_list(request: Request):
    '''
    IP로 파싱 요청 리스트를 보여준다.

    '''
    private_dir = os.path.join(TMP_PATH, request.client.host)
    
    dirs = [f for f in os.listdir(private_dir)]

    sub_path_n_file_list = get_1_depth_sub_path_n_file_list_by_extensions(private_dir, [r'*.yml'])

    ret = []
    for sub_path, file_list in sub_path_n_file_list:
        if len(file_list) == 0:
            continue
        filename = os.path.basename(file_list[0])
        filename = os.path.splitext(filename)[0]
        ret.append([sub_path, filename])
        
    return ret


@router.delete('/request/{timestamp}')
async def delete_delete(
    timestamp: str,
    request: Request,
    current_user: Annotated[User, Security(get_current_active_user, scopes=['deletedocu'])],
):
    private_dir = os.path.join(TMP_PATH, request.client.host)
    workplace_dir = os.path.join(private_dir, timestamp)
    shutil.rmtree(workplace_dir)
    return None


@router.post("/main/request/{timestamp}/download")
async def get_main_request_download(timestamp: str, request: Request):
    '''
    결과 파일을 다운로드
    '''
    private_dir, workplace_dir, meta = await get_meta(timestamp, request)
    
    params = await request.json()

    if '..' in params['filename']:
        raise Exception('Abnormal activity')
    
    file_path = os.path.join(workplace_dir, params['filename'])

    # access-control-expose-headers 는 axios를 위해서 추가해준다.
    return FileResponse(file_path, media_type='application/octet-stream', filename=params['filename'], headers={"access-control-expose-headers": ("Content-Disposition")})

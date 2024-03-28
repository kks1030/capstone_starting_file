# Datatool API Server

## Installation

루트 폴더로 이동하여 아래 명령 실행

윈도우
```
python -m venv .venv311

.\.venv311\Scripts\Activate.ps1

pip install -r requirements.txt
```

<br>

리눅스
```
python -m venv .venv311

. .venv311/bin/activate

pip install -r requirements.txt
```

<br>

## 터미널에서 디버깅 방법

<br>

0. vscode 로 client_app 또는 server_app 실행

<br>

1-1. client_app를 vscode로 실행한 경우 server_app는 명령어로 실행

```
.venv311/bin/uvicorn server:app --port 8086 --reload --log-config resources/config/server/server.ini
```

1-2. server_app를 vscode로 실행한 경우 client_app는 명령어로 실행
```
cd client_app
npm run dev
```

<br>


## vscode를 이용해서 디버깅 하는 방법

1. vscode 설치

2. 터미널을 열고 이 파일이 있는 경로로 이동

3. code 명령으로 vscode 열기

```sh
code .
```

5. 왼쪽 `Run and Debug` 탭을 눌르고 원하는 명령 선택

6. 세부 조정이 필요하다면 Ctrl + P를 누르고 `launch.json`를 선택하여 수정

6. F5키를 눌러시 실행

<br>


## Scopes

- services/auth.py 참조

<br>


## 절대경로 vs 상대경로 설명

절대 경로는 어디서 호출하던 맞는 경로이고 상대 경로는 사용자가 특정 디렉토리에 들어가 있을때만 맞는 상대적인 경로입니다.

예를 들어 `/home/voctree/workspaces`는 `/`로 시작하기 때문에 절대경로이고,

`./workspaces`는 `/`로 시작하지 않고 `.`로 시작하기 때문에 상대경로입니다.

`.` 은 현재 경로를 뜻합니다.

파일을 표시할때도 동일한 규칙을 가집니다.

<br>

lang | 설명
---|---
`ko` | 한글
`en` | 영어
`zh_CN` | 중국어간체
`zh_TW` | 중국어번체
`ja` | 일본어

<br>

# 버전에 맞게 CUDA 설치하는 법

pyTorch 사이트에서 가서 설치 가능한 버전을 찾아본다.

pyTorch 를 설치한다.

pyTorch 설치 버전을 찾았으면 그에 맞는 cuda toolkit 을 다운로드 설치한다.

아래 명령을 실행해서 cuda가 잘 동작하는지 확인한다.

```
import torch

torch.cuda.is_available()
```

<br>


# 윈도우에서 Mecab 설치하는 방법

https://wonhwa.tistory.com/49

위 링크 설명이 잘되어있으나 우리 실행환경과 달라서 3, 5번은 아래 설명을 보고 진행합니다.

1. "C:\"에 mecab 폴더 만들어 주기

2.  mecab-ko-msvc 설치 및 mecab 폴더에 압축해제

3. mecab-ko-dic-msv 설치 및 mecab 폴더에 압축해제

4. ~~anaconda로 가상환경 만들고 파이썬 3.8버전으로 설치하기~~ 3.8버전으로 가상환경 만들기

```sh
python3.8 -m venv .venv38
```

5. python wheel 다운받고 설치하기

설치 경로

```bash
.venv38\Lib\site-packages
```

설치 하기

```bash
.venv38\Scripts\activate.ps1

pip install .venv38\Lib\site-packages\mecab_python-0.996_ko_0.9.2_msvc-cp311-cp311-win_amd64.whl

pip install konlpy
```

<br>

# Ubuntu에서 Mecab 설치하는 방법

```sh
pip install python-mecab-ko
```

<br>

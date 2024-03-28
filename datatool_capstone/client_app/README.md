# 데이터 저작도구 Frontend


## 시작하기전에

vite 버그인지 Windows에서는 vite 변수가 안 먹힘.

```
axios.defaults.baseURL = import.meta.env.VITE_API_URL

axios.defaults.baseURL == undefined
```

VITE_API_URL를 하드코딩하던지 WSL를 사용하기를 권장함.

Windows 에서 import.meta.env 로 시작하는 모든 코드를 하드코딩하던지 해야함.


Linux에서는 잘 동작하는데, 환경설정 파일은 각각로 나누어짐

```
.env.dev
.env.production
```

<br>

## Installation

### Node, npm 설치

Windows는 인터넷에서 msi 파일을 [다운로드](https://nodejs.org/en/download)

Linux는 아래 명령으로 설치

```sh
sudo snap install node --classic
```

package 설치는  폴더에서

Windows
```sh
cd client_app
npm i
```

Linux
```sh
cd client_app
/snap/bin/npm i
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

## Note

```
npm create vite@latest

npm i

npm install -D tailwindcss@latest postcss@latest autoprefixer@latest

npx tailwindcss init -p

```

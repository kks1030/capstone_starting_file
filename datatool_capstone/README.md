# 데이터 저작도구

## 실행법

Backend는 .venv311에 Linux에서 만든 폴더여야 한다. 결과적으로는 `.venv311/Scripts/python.exe`가 아닌 `.venv311/bin/python3.11`을 실행해야함.


0. docufront에서 참조하는 서버의 주소가 제대로 되었는지 확인
 - main.js 의 axios.defaults.baseURL 확인
 - nginx 설정 확인

<br>

1. docufront 빌드
```
cd client_app
npm run build
```

<br>

2. docker-compose 실행

 - 최초 기동
```
docker-compose up --build
```

 - 재기동
```
docker-compose down && docker-compose up -d
```

<br>

3. 접속
 - http://127.0.0.1:8088

<br>
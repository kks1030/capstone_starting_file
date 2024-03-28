FROM python:3.11

# source 명령이 먹히게 하려면 실행
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

WORKDIR /app

## .venv311을 그대로 이용할 거라 명령을 실행하지 않아도 됨
#COPY ./requirements-fastapi.txt /code/requirements-fastapi.txt
#RUN pip install --upgrade pip
#RUN pip install --no-cache-dir --upgrade -r /code/requirements-fastapi.txt
#RUN python -m spacy download en_core_web_sm


# Mecab 설치
# RUN apt-get install -y curl git
# RUN bash <(curl -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh)
# RUN apt-get remove --purge -y curl git


# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
# CMD ["uvicorn", "server:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80", "--workers", "4"]


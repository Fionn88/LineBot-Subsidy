FROM python:3.8.6-buster

WORKDIR /app

ADD LocalFakeData/ /app

RUN pip install --no-cache-dir -r requirements.txt
ENV run_env=docker
CMD python3 main.py

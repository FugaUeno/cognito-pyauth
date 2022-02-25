FROM python:3.9.9-slim-buster

WORKDIR /root/app

RUN apt update && \
    apt upgrade -y && \
    apt install -y git && \
    apt clean

RUN pip install poetry && \
    poetry config virtualenvs.in-project true && \
    poetry config virtualenvs.create true

# syntax=docker/dockerfile:1
FROM python:3.6-slim-stretch
ENV DJANGO_SETTINGS_MODULE=market.settings
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/
RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.3/zsh-in-docker.sh)"

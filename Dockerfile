FROM python:3.11.2-slim-buster

LABEL maintainer="DDCroft <ddc.dev.python@gmail.com>"
LABEL version="1.0"
LABEL description="Notification-Services"

WORKDIR /notif-service/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH .:/notif-service/

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
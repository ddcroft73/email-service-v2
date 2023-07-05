
FROM python:3.11.2-slim-buster

LABEL maintainer="Danny Croft <ddc.dev.python@gmail.com>"
LABEL version="1.0"
LABEL description="Email-service v2"

WORKDIR usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8014", "--reload"]

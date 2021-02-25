FROM python:3.8.2-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip
RUN apk add --no-cache jpeg-dev zlib-dev
RUN apk add --no-cache --virtual .build-deps build-base linux-headers
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

CMD gunicorn parents_back.wsgi:application --bind 0.0.0.0:8000

COPY . /usr/src/app/
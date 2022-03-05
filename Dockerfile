FROM python:3.7-alpine
MAINTAINER Rafito from Polska Elmi

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D course
USER course

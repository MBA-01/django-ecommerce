FROM debian:stable-slim

FROM python:3
ENV PYTHONUNBEFFERED 1

RUN mkdir /app

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app/
FROM python:3.11-slim

COPY . ./remarcable-application

WORKDIR /remarcable-application

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python manage.py migrate

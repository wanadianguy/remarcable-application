FROM python:3.11-slim

COPY . ./catalog

WORKDIR /catalog

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python manage.py migrate

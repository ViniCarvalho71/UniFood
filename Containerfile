FROM python:3.12-alpine 

RUN python -m pip install django==5

RUN mkdir /app
WORKDIR /app
COPY . .
EXPOSE 8000
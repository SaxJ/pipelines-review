FROM python:3

COPY pipelines_notify.py .
COPY pipelines_requirements .

RUN ["pip", "install", "-r", "pipelines_requirements"]

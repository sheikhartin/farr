FROM python:3.10-slim

RUN apt-get update && apt-get install -y coreutils

WORKDIR /app

COPY . /app

ENV FARRPATH /app

RUN pip install poetry

RUN poetry build && poetry install

ENTRYPOINT ["python", "-m", "farr"]

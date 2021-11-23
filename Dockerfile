FROM python:3.8-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /workspace

COPY poetry.lock pyproject.toml ./

RUN apt update && apt install git -y

RUN pip install poetry

RUN poetry config virtualenvs.create false \
    && poetry install

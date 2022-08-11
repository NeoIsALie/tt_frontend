FROM python:3.10-slim as python_base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # Poetry no venv
    POETRY_VIRTUALENVS_CREATE=false \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \

    APP_PATH="/opt/app" \

    LC_ALL=ru_RU.UTF-8 \
    LANG=ru_RU.UTF-8

WORKDIR $APP_PATH
COPY poetry.lock pyproject.toml ./

RUN apt-get update && apt-get install -y --no-install-recommends build-essential libpq-dev curl

RUN pip install poetry; \
    pip install psycopg2-binary --no-binary psycopg2-binary; \
    poetry install --no-dev;


FROM python_base as prod

WORKDIR $APP_PATH

# Файлы приложения.
COPY ./app ./app
COPY ./main.py ./main.py
COPY ./deploy/entrypoints/*.sh ./

ENTRYPOINT sh start_app.sh

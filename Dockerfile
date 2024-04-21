# https://medium.com/@albertazzir/blazing-fast-python-docker-builds-with-poetry-a78a66f5aed0
FROM python:3.12-bullseye as builder

RUN pip install poetry==1.8.2

ENV POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_IN_PROJECT=1 \
  POETRY_VIRTUALENVS_CREATE=1 \
  POETRY_CACHE_DIR=/tmp/poetry_cache

# break when enabling this
WORKDIR /app

COPY pyproject.toml poetry.lock config.yaml README.md ./

RUN poetry config virtualenvs.create false --local
RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

COPY peterpy ./peterpy

RUN poetry install --without dev

# Run Application
CMD [ "poetry", "run", "python", "-m", "peterpy" ]
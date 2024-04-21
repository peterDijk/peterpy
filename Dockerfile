# https://medium.com/@albertazzir/blazing-fast-python-docker-builds-with-poetry-a78a66f5aed0
FROM python:3.12 as python-base

RUN pip install poetry==1.8.2

# WORKDIR /app

COPY pyproject.toml poetry.lock config.yaml README.md ./
COPY peterpy ./peterpy

RUN poetry config virtualenvs.create false --local
RUN poetry install --without dev

# Run Application
CMD [ "poetry", "run", "python", "-m", "peterpy" ]
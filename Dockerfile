FROM python:3

USER root

WORKDIR /app

# Copy build-system
RUN pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create true --local
RUN poetry config virtualenvs.in-project true --local

# Copy main app
COPY --chown=root:root peterpy /app/peterpy
COPY --chown=root:root ./pyproject.toml /app/pyproject.toml
COPY --chown=root:root ./poetry.lock /app/poetry.lock
COPY --chown=root:root ./config.yaml /app/config.yaml
COPY --chown=root:root ./pylintrc /app/pylintrc
COPY --chown=root:root ./README.md /app/README.md

# Pre-fill venv
RUN poetry install --no-root --without dev

# RUN poetry build

# COPY . .

# CMD [ "python", "./your-daemon-or-script.py" ]
# CMD [ "poetry run peterpy"]
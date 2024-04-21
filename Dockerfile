FROM python:3.12 as python-base

RUN pip install poetry
COPY . .
RUN poetry config virtualenvs.create false --local
RUN poetry install

# Run Application
CMD [ "poetry", "run", "python", "-m", "peterpy" ]
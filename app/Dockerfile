FROM python:3.11.4-slim as python-base
RUN mkdir /app
WORKDIR  /app
COPY /pyproject.toml /app
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install
COPY . .
CMD gunicorn -k uvicorn.workers.UvicornWorker --worker-tmp-dir /dev/shm --log-level debug src.main:app --bind=0.0.0.0:7000
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim-2021-10-02
COPY ./app /app
WORKDIR /app
ENV ENV dev

RUN pip install -r requirements.txt
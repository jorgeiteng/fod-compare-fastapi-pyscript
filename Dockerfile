# docker build . --tag api.fod:2023
FROM python:3.11

WORKDIR /src
COPY . /src
RUN pip install -r requirements.txt

CMD uvicorn fod-sample-info:app --host 0.0.0.0 --port 8000 --reload

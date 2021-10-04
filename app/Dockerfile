FROM python:3.9-alpine

RUN apk add build-base
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD [ "gunicorn", "-w 3", "-t 3", "-k uvicorn.workers.UvicornWorker", "-b 0.0.0.0:8000", "main:app", "--timeout 90"]
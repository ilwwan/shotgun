FROM python:3.9

COPY . .
RUN pip install psycopg2-binary
ENTRYPOINT [ "python", "test.py" ]
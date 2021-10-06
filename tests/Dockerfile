FROM python:3.9

RUN pip install psycopg2-binary
RUN pip install asyncio

COPY ./test.py .


ENTRYPOINT [ "python", "test.py"]
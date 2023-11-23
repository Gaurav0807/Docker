FROM python:3.8

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && \
    apt-get install -y postgresql-client libpq-dev

RUN pip install psycopg2-binary

CMD ["python", "./ingestion.py"]

# Building a Data Engineering Pipeline with Docker and Airflow

## Introduction

In today's data-driven world, the ability to efficiently process, validate, and analyze data is paramount. This blog post will guide you through creating a comprehensive data engineering solution using Docker and Apache Airflow. We will explore the architecture, key components, and real-world use cases of this setup while providing a step-by-step guide to run it locally.

## Problem Statement

Data engineering often involves a series of complex tasks, including data ingestion, transformation, validation, and storage. Managing these tasks can be cumbersome without a well-structured pipeline. Traditional methods can lead to several challenges, such as:

- Difficulty in scaling operations
- Lack of visibility into data processing
- Challenges in managing dependencies between tasks

To address these challenges, we will create a robust data engineering pipeline that automates the entire workflow using Docker containers and Apache Airflow.

## Architecture Overview

The architecture of our data engineering solution consists of multiple components:

1. **Docker**: Containerizes our application, making it easy to deploy and manage.
2. **PostgreSQL**: A relational database to store our processed data.
3. **Apache Airflow**: An orchestration tool that manages the execution of our data pipeline tasks.
4. **PgAdmin**: A web-based interface for managing PostgreSQL databases.

These components are interconnected through Docker Compose, ensuring seamless communication between them.

## Key Components

### 1. Docker Compose Configuration

The `docker-compose.yaml` file defines our services, which include PostgreSQL, PgAdmin, and our data engineering application. Here’s a sample configuration:

```yaml
version: '3'

services:
  postgres:
    image: postgres:latest
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
      POSTGRES_DB: mydatabase
    ports:
      - "5432:5432"
    volumes:
      - pg_data:/var/lib/postgresql/data

  pgadmin:
    image: dpage/pgadmin4
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@example.com
      PGADMIN_DEFAULT_PASSWORD: admin
    ports:
      - "5050:80"
    depends_on:
      - postgres

  data_engineering_project:
    build: .
    depends_on:
      - postgres
    environment:
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=mydatabase

volumes:
  pg_data:
```

### 2. Data Ingestion Script

The `ingestion.py` script generates synthetic data and loads it into our PostgreSQL database. Below is an example of what this script might look like:

```python
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

# Database connection parameters
POSTGRES_HOST = "postgres"
POSTGRES_PORT = "5432"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "password"
POSTGRES_DB = "mydatabase"

# Generate synthetic data
data = {
    'Name': np.random.choice(['Alice', 'Bob', 'Charlie'], size=10),
    'Age': np.random.randint(20, 40, size=10),
    'Salary': np.random.randint(30000, 80000, size=10),
}

df = pd.DataFrame(data)
df['Age'] += 5
df['Salary'] += 10000

# Save to CSV
df.to_csv('/app/output_data.csv', index=False)

# Load data into PostgreSQL
engine = create_engine(f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}')
df.to_sql('employee_data', engine, index=False, if_exists='replace')

print("Data engineering process completed.")
```

### 3.
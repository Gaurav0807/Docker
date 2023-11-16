# data_engineering.py

import pandas as pd
import numpy as np
from sqlalchemy import create_engine


POSTGRES_HOST = "postgres"
POSTGRES_PORT = "5432"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "password"
POSTGRES_DB = "mydatabase"

data = {
    'Name': np.random.choice(['Alice', 'Bob', 'Charlie'], size=10),
    'Age': np.random.randint(20, 40, size=10),
    'Salary': np.random.randint(30000, 80000, size=10),
}

df = pd.DataFrame(data)

df['Age'] = df['Age'] + 5
df['Salary'] = df['Salary'] + 10000

df.to_csv('/app/output_data.csv', index=False)


engine = create_engine(
    f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
)
df.to_sql('employee_data', engine, index=False, if_exists='replace')

print("Data engineering process completed.")

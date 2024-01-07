# my_data_dag.py

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
import os
from validator import validate_and_save_data


python_script_path = "/opt/airflow/jobs/data_quality_check.py"


default_args = {
    'owner': 'Gaurav',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'my_data_processing_dag',
    default_args=default_args,
    description='A simple DAG to process data',
    schedule_interval=timedelta(days=1),  # Set the frequency of DAG runs
)


start_task = DummyOperator(
    task_id='start_task',
    dag=dag,
)


end_task = DummyOperator(
    task_id='end_task',
    dag=dag,
)



process_data_task = PythonOperator(
    task_id='process_data_task',
    python_callable=validate_and_save_data,
    dag=dag,
    #op_kwargs={"file_path": "/opt/airflow/jobs/taxi_data.csv","postgres_url":"postgresql://airflow:airflow@postgres:5432/airflow","table_name":"data_quality"},
)

# Set the task dependencies
start_task >> process_data_task >> end_task

if __name__ == "__main__":
    dag.cli()

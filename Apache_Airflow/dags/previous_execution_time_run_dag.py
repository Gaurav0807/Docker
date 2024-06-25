from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

default_args = {
    'owner': 'Gaurav Rawat',
    'depends_on_past': False,
    'start_date': datetime(2024, 6, 14),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def hello():
    print("Hello Airflow DAG")

def calculate_next_runtime(execution_date, **kwargs):
    next_runtime = execution_date + timedelta(minutes=3)
    return next_runtime.isoformat()

dag = DAG(
    'previous_execution_time_run_dag',
    default_args=default_args,
    schedule_interval=None,
    description="Run Airflow DAG every 3 minutes based on previous execution time"
)

start = DummyOperator(task_id='start', dag=dag)

python_task = PythonOperator(
    task_id='python_task',
    python_callable=hello,
    dag=dag,
)

calculate_next_runtime_task = PythonOperator(
    task_id='calculate_next_runtime_task',
    python_callable=calculate_next_runtime,
    provide_context=True,
    dag=dag
)

trigger_next_run = TriggerDagRunOperator(
    task_id='trigger_next_run',
    trigger_dag_id='previous_execution_time_run_dag',
    execution_date='{{ task_instance.xcom_pull(task_ids="calculate_next_runtime_task") }}',
    reset_dag_run=True, # Resets the state of the triggered DAG run to allow it to run again.
    wait_for_completion=False, # Setting this to False ensures that the current DAG run does not wait for the triggered DAG run
                                # to complete before proceeding to the next tasks
    dag=dag,
)

end = DummyOperator(task_id='end', dag=dag)

start >> python_task >> calculate_next_runtime_task >> trigger_next_run >> end

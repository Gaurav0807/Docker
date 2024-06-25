from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator


default_args = {
    'owner': 'Gaurav Rawat',
    'depends_on_past': False,
    'start_date': datetime(2024,6,14),
    'retries':1,
    'retries_delay': timedelta(minutes=5),
}
def push_function(**kwargs):
    kwargs['ti'].xcom_push(key='test_key',value='Hii Gaurav Rawat')

def pull_function(**kwargs):
    value = kwargs['ti'].xcom_pull(key='test_key',task_ids='push_task')

    print(f"Value pulled from xcom: {value}")

dag = DAG(
    'XCOM_DAG',
    default_args=default_args,
    description="Airflow DAG for XCOM ",
    schedule_interval=timedelta(days=1)
)


start_task = DummyOperator(task_id ="start_task",dag=dag)


push_task = PythonOperator(
    task_id='push_task',
    provide_context=True,
    python_callable=push_function,
    dag=dag,
)

pull_task = PythonOperator(
    task_id='pull_task',
    provide_context=True,
    python_callable=pull_function,
    dag=dag,
)

start_task >> push_task >> pull_task
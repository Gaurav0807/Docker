

from datetime import datetime,timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

default_args = {
	'owner':'Gaurav',
	'depends_on_past':False,
	'start_date': datetime(2024,1,6),
	'retries':1,
	'retries_delay': timedelta(minutes=5),
}

dag = DAG(
	'Testing',
	default_args=default_args,
	description='Simple dag creation',
	schedule_interval=timedelta(days=1)
)


start_task = DummyOperator(task_id='start_task',dag = dag)

def print_hello():
	print("Hello this is testing airflow_dag")

hey_task = PythonOperator(
	task_id='hey_task',
	python_callable=print_hello,
	dag=dag,
)

end_task = DummyOperator(task_id='end_task',dag = dag)

start_task >> hey_task >> end_task

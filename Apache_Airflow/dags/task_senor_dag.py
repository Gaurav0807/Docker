from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.sensors.external_task import ExternalTaskSensor

default_args = {
    'owner': 'Gaurav Rawat',
    'depends_on_past': False,
    'start_date': datetime(2024,6,14),
    'retries':1,
    'retries_delay': timedelta(minutes=5),
}

def start_func():
    print("External Task Dependency Sensor is Starting....... ")

dag = DAG(
    'task_senor_dag',
    default_args=default_args,
    schedule_interval=timedelta(days=1),
    description= "Testing Task Dependency Sensor"
)


start = PythonOperator(task_id="start",
                    python_callable = start_func,
                    dag=dag)


external_task_dag = ExternalTaskSensor(
    task_id='external_task_dag',
    external_dag_id='XCOM_With_Variable_DAG',
    external_task_id='branching',
    mode='poke',
    execution_delta=timedelta(minutes=4),#Difference between current dag time minus external dag time
    poke_interval=60, #Check every 60 seconds
    timeout=600,
    dag=dag,
)

end_task = DummyOperator(task_id ="end_task",dag=dag)


start >> external_task_dag >> end_task
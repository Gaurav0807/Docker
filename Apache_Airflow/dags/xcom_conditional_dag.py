from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator



default_args = {
    'owner': 'Gaurav Rawat',
    'depends_on_past': False,
    'start_date': datetime(2024,6,14),
    'retries':1,
    'retries_delay': timedelta(minutes=5),
}

def push_function(**kwargs):

    value = 'condition_met'

    kwargs['ti'].xcom_push(key='test_key',value=value)

def check_condition(**kwargs):
    value = kwargs['ti'].xcom_pull(task_ids='push_task',key='test_key')

    if value == 'condition_met':
        return 'true_task'
    else:
        return 'false_task'




dag = DAG(
    'XCOM_Condition_DAG',
    default_args=default_args,
    description="Airflow DAG for XCOM ",
    schedule_interval=timedelta(days=1)
)


start_task = DummyOperator(task_id ="start_task",dag=dag)


push_task = PythonOperator(
    task_id='push_task',
    provide_context=True,
    python_callable=push_function,
    dag=dag
)

branching = BranchPythonOperator(
    task_id='branching',
    provide_context=True,
    python_callable=check_condition,
    dag=dag
)

true_task = DummyOperator(
    task_id = 'true_task',
    dag=dag
)

false_task = DummyOperator(
    task_id = 'false_task',
    dag=dag
)

start_task >> push_task >> branching
branching >> [true_task, false_task ]
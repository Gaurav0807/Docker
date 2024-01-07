import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator



dag = DAG(
    dag_id = "Basic_dag",
    default_args = {
        "owner": "Gaurav",
        "start_date": airflow.utils.dates.days_ago(1)
    },
    schedule_interval = "@daily"
)

def my_python_function():
    print("Hello, World!")

start = PythonOperator(
    task_id='start',
    python_callable=my_python_function,
    dag=dag
)


# end = PythonOperator(
#     task_id='end',
#     python_callable= lambda: print("Jobs Ended"),
#     dag=dag
# )

start
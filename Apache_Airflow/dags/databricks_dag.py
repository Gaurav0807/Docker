from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksSubmitRunOperator
from datetime import datetime,timedelta
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

default_args = {
    'owner': 'Gaurav Rawat',
    'depends_on_past' :False,
    'start_date': datetime(2024,6,14),
    'retries':1,
    'retries_delay': timedelta(minutes=5),
}

with DAG('databricks_cluster_dag',
         default_args=default_args,
         schedule_interval=None,
         description="Databricks All purpose Cluster",
         catchup=False) as dag:
    
    cluster_config = {
        'spark_version': '2.1.0-db3-scala2.11',
        'node_type_id': 'r3.xlarge',
        'aws_attributes': {'availability': 'ON_DEMAND'},
        'num_workers': 8,
        }
    
    notebook_task_params = {
            'notebook_path': '/Users/dbtest@gmail.com/Testingdata',   # Notebook Tasks
        }
    
    databricks_notebook = DatabricksSubmitRunOperator(
        task_id = 'databricks_notebook',
        databricks_conn_id="databricks_default",
        cluster_id=cluster_config,
        notebook_task = notebook_task_params,
    )

    databricks_notebook


    
    




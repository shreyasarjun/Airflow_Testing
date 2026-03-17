from datetime import datetime
import subprocess
from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator

def docker_ps():
    result = subprocess.run(['docker', 'ps'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print("Docker PS Output:\n" + result.stdout)
    if result.stderr:
        print("Docker PS Error:\n" + result.stderr)

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
}

dag = DAG(
    'dag4',
    default_args=default_args,
    schedule=None,
    catchup=False
)

docker_ps = PythonOperator(
    task_id='docker_ps',
    python_callable=docker_ps,
    dag=dag
)

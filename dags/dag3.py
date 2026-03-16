import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.base import BaseHook
from airflow.settings import Session
from airflow.models import DagRun
from datetime import datetime


def read_env_and_db():

    # Environment variable
    env_name = os.getenv("APP_ENV", "local")
    print(f"Running environment: {env_name}")

    # Connection example
    conn = BaseHook.get_connection("postgres_default")
    print(f"Connection host: {conn.host}")

    # Direct metadata DB access (this will break in Airflow 3)
    session = Session()
    dag_runs = session.query(DagRun).limit(5).all()

    print(f"Total dag runs fetched: {len(dag_runs)}")


with DAG(
    dag_id="migration_dag_env_connection_db",
    start_date=datetime(2026, 3, 15),
    schedule_interval="@hourly",
    catchup=False,
) as dag:

    task1 = PythonOperator(
        task_id="read_env_connection_db",
        python_callable=read_env_and_db,
    )
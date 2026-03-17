import os
import requests
from datetime import datetime

from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.sdk import BaseHook


def get_jwt_token():
    response = requests.post(
        "http://data-engg_6dbc83-api-server-1:8080/auth/token",
        json={"username": "admin", "password": "admin"},
        headers={"Content-Type": "application/json"}
    )
    response.raise_for_status()
    return response.json()["access_token"]


def read_env_and_db():
    # Environment variable
    env_name = os.getenv("APP_ENV", "local")
    print(f"Running environment: {env_name}")

    # Connection example
    conn = BaseHook.get_connection("postgres_default")
    print(f"Connection host: {conn.host}")

    # ✅ Use API instead of ORM in Airflow 3
    token = get_jwt_token()

    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(
        "http://data-engg_6dbc83-api-server-1:8080/api/v2/dags/migration_dag_env_connection_db/dagRuns",
        headers=headers,
        params={"limit": 5}
    )
    response.raise_for_status()

    dag_runs = response.json().get("dag_runs", [])
    print(f"Total dag runs fetched: {len(dag_runs)}")

    for run in dag_runs:
        print(f"Run ID: {run['dag_run_id']} | State: {run['state']}")


with DAG(
    dag_id="migration_dag_env_connection_db",
    start_date=datetime(2026, 3, 15),
    schedule="@hourly",
    catchup=False,
) as dag:

    read_env_connection_db = PythonOperator(
        task_id="read_env_connection_db",
        python_callable=read_env_and_db,
    )
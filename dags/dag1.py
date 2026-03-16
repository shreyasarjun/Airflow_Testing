from airflow import DAG
from airflow.providers.http.operators.http import HttpOperator
from airflow.models import Variable
from datetime import datetime


API_ENDPOINT = Variable.get("sample_api_endpoint", default_var="posts/1")

with DAG(
    dag_id="migration_dag_api_variable",
    start_date=datetime(2026, 3, 15),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    call_api = HttpOperator(
        task_id="call_api",
        http_conn_id="sample_api_conn",
        endpoint=API_ENDPOINT,
        method="GET",
        log_response=True,
    )
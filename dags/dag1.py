from airflow.providers.http.operators.http import HttpOperator
from datetime import datetime
from airflow.sdk import DAG

API_ENDPOINT = "{{ var.value.sample_api_endpoint}}"

with DAG(
    dag_id="migration_dag_api_variable",
    start_date=datetime(2026, 3, 15),
    schedule="@daily",
    catchup=False,
) as dag:

    call_api = HttpOperator(
        task_id="call_api",
        http_conn_id="sample_api_conn",
        endpoint=API_ENDPOINT,
        method="GET",
        log_response=True,
    )
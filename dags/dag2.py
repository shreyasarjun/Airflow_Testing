from datetime import datetime
from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.sdk import get_current_context


def push_data():
    context = get_current_context()

    logical_date = context["logical_date"]
    ds = context["ds"]

    print(f"Logical date: {logical_date}")
    print(f"DS value: {ds}")

    return {"status": "data_processed", "date": ds}


def pull_data():
    context = get_current_context()
    ti = context["ti"]

    data = ti.xcom_pull(task_ids="push_task")
    print(f"Received XCom data: {data}")


with DAG(
    dag_id="migration_dag_context_xcom",
    start_date=datetime(2026, 3, 15),
    schedule="0 12 * * *",
    catchup=False,
) as dag:

    push_task = PythonOperator(
        task_id="push_task",
        python_callable=push_data,
    )

    pull_task = PythonOperator(
        task_id="pull_task",
        python_callable=pull_data,
    )

    push_task >> pull_task
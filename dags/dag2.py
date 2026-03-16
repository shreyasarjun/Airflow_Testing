from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime


def push_data(**context):
    execution_date = context["execution_date"]
    ds = context["ds"]

    print(f"Execution date: {execution_date}")
    print(f"DS value: {ds}")

    return {"status": "data_processed", "date": ds}


def pull_data(**context):
    ti = context["ti"]

    data = ti.xcom_pull(task_ids="push_task")
    print(f"Received XCom data: {data}")


with DAG(
    dag_id="migration_dag_context_xcom",
    start_date=datetime(2026, 3, 15),
    schedule_interval="0 12 * * *",
    catchup=False,
) as dag:

    push_task = PythonOperator(
        task_id="push_task",
        python_callable=push_data,
        provide_context=True,
    )

    pull_task = PythonOperator(
        task_id="pull_task",
        python_callable=pull_data,
        provide_context=True,
    )

    push_task >> pull_task
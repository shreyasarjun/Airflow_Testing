from datetime import datetime
import os
import socket
import platform
from airflow import DAG
from airflow.operators.python import PythonOperator

def log_execution_environment():
    print("Execution Environment Information:")
    print(f"Hostname: {socket.gethostname()}")
    print(f"Platform: {platform.platform()}")
    print(f"System: {platform.system()}")
    print(f"Release: {platform.release()}")
    print(f"Python Version: {platform.python_version()}")
    print(f"Current Working Directory: {os.getcwd()}")
    print(f"Environment Variables: {os.environ}")

    # Try to detect if running inside Docker
    try:
        with open('/proc/1/cgroup', 'rt') as f:
            cgroup_content = f.read()
        if 'docker' in cgroup_content or 'containerd' in cgroup_content:
            print("Likely running inside a Docker container.")
            # Try to get container ID
            for line in cgroup_content.splitlines():
                if 'docker' in line or 'containerd' in line:
                    print(f"Container cgroup line: {line}")
        else:
            print("Not running inside a Docker container (no docker/containerd in /proc/1/cgroup).")
    except Exception as e:
        print(f"Could not read /proc/1/cgroup: {e}")

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

log_env_task = PythonOperator(
    task_id='log_execution_environment',
    python_callable=log_execution_environment,
    dag=dag
)

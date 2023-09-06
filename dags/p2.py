from datetime import timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import datetime
from airflow.utils.dates import timedelta
from airflow.models import Variable

PROJECT_ROOT_PATH=Variable.get("PROJECT_ROOT_PATH")
PROFILE="jaffle_shop"
TARGET_ENV="prod"

default_args = {
    'owner': 'admin',
    'depends_on_past': False,
    'start_date': datetime(2023, 8, 28),
    'email': [],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}
with DAG(
    dag_id='dbt_dag',
    default_args=default_args,
    description='An Airflow DAG to invoke simple dbt commands',
    schedule_interval=timedelta(days=1),
):

    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command=f'cd {PROJECT_ROOT_PATH} && dbt run --profiles-dir {PROJECT_ROOT_PATH} --profile {PROFILE} --target {TARGET_ENV}',
        env={'DBT_ACCESS_TOKEN': DBT_ACCESS_TOKEN},
        append_env=True,
        dag=dag,
    )

    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command=f'cd {PROJECT_ROOT_PATH} && dbt test --profiles-dir {PROJECT_ROOT_PATH} --profile {PROFILE} --target {TARGET_ENV}',
        env={'DBT_ACCESS_TOKEN': DBT_ACCESS_TOKEN},
        append_env=True,
        dag=dag,
    )

    dbt_run >> dbt_test
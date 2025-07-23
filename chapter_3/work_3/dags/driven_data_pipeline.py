from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime

import sys
sys.path.append('/opt/airflow/data')

from save_raw_data import save_raw_data


# Define the default arguments for DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 0,
}

# Define the DAG
dag = DAG(
    'extract_raw_data_pipeline',
    default_args=default_args,
    description='DataDriven Main Pipeline.',
    schedule_interval="0 7 * * *",  # 7:00 AM every day
    start_date=datetime(2024, 9, 22),
    catchup=False,
)

# Task 1: Extract raw data
extract_raw_data_task = PythonOperator(
    task_id='extract_raw_data',
    python_callable=save_raw_data,
    dag=dag,
)

# Task 2: Create raw schema
create_raw_schema_task = PostgresOperator(
    task_id='create_raw_schema',
    postgres_conn_id='postgres_conn',
    sql='CREATE SCHEMA IF NOT EXISTS driven_raw;',
    dag=dag,
)

# Task 3: Create raw table
create_raw_table_task = PostgresOperator(
    task_id='create_raw_table',
    postgres_conn_id='postgres_conn',
    sql="""
    CREATE TABLE IF NOT EXISTS driven_raw.raw_batch_data (
        person_name VARCHAR(100),
        user_name VARCHAR(100),
        email VARCHAR(100),
        personal_number NUMERIC,
        birth_date VARCHAR(100),
        address VARCHAR(100),
        phone VARCHAR(100),
        mac_address VARCHAR(100),
        ip_address VARCHAR(100),
        iban VARCHAR(100),
        accessed_at TIMESTAMP,
        session_duration INT,
        download_speed INT,
        upload_speed INT,
        consumed_traffic INT,
        unique_id VARCHAR(100)
    );
    """,
    dag=dag,
)

# Task 4: Load CSV data into the table
load_raw_data_task = PostgresOperator(
    task_id='load_raw_data',
    postgres_conn_id='postgres_conn',
    sql="""
    COPY driven_raw.raw_batch_data(
        person_name, user_name, email, personal_number, birth_date,
        address, phone, mac_address, ip_address, iban, accessed_at,
        session_duration, download_speed, upload_speed, consumed_traffic,
        unique_id
    )
    FROM '/opt/airflow/data/raw_data.csv'
    DELIMITER ','
    CSV HEADER;
    """,
    dag=dag,
)

# Task 5: Run dbt staging models
run_dbt_staging_task = BashOperator(
    task_id='run_dbt_staging',
    bash_command='set -x; cd /opt/airflow/dbt && dbt run --select tag:staging',
    dag=dag,
)

# Task 6: Run dbt trusted models
run_dbt_trusted_task = BashOperator(
    task_id='run_dbt_trusted',
    bash_command='set -x; cd /opt/airflow/dbt && dbt run --select tag:trusted',
    dag=dag,
)

# Set task dependencies
[extract_raw_data_task, create_raw_schema_task] >> create_raw_table_task
create_raw_table_task >> load_raw_data_task >> run_dbt_staging_task
run_dbt_staging_task >> run_dbt_trusted_task

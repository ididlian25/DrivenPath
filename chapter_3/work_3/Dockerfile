# Usa la imagen oficial de Airflow como base
FROM apache/airflow:2.10.2

# Cambia al usuario airflow
USER airflow

# Copia el archivo de requerimientos
COPY requirements.txt .

# Instala las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Asegura que la carpeta dbt esté presente
COPY dbt /opt/airflow/dbt

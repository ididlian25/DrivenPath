import random
import csv
import logging
import uuid
import polars as pl

from faker import Faker
from datetime import datetime, timedelta

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[logging.StreamHandler()]
)

def create_data(locale: str) -> Faker:
    """Crea una instancia de Faker con la configuración regional deseada."""
    logging.info(f"Creando datos sintéticos para el país: {locale}")
    return Faker(locale)

def generate_record(fake: Faker) -> list:
    """Genera un solo registro de usuario falso."""
    person_name = fake.name()
    user_name = person_name.replace(" ", "").lower()
    email = f"{user_name}@{fake.free_email_domain()}"
    personal_number = fake.ssn()
    birth_date = fake.date_of_birth()
    address = fake.address().replace("\n", ", ")
    phone = fake.phone_number()
    mac_address = fake.mac_address()
    ip_address = fake.ipv4()
    iban = fake.iban()
    accessed_at = fake.date_time_between("-1y", "now")
    session_duration = random.randint(0, 36_000)
    download_speed = random.randint(0, 1_000)
    upload_speed = random.randint(0, 800)
    consumed_traffic = random.randint(0, 2_000_000)

    return [
        person_name, user_name, email, personal_number, birth_date,
        address, phone, mac_address, ip_address, iban, accessed_at,
        session_duration, download_speed, upload_speed, consumed_traffic
    ]

def write_to_csv(file_path: str, rows: int) -> None:
    """Escribe múltiples registros falsos en un archivo CSV."""
    fake = create_data("ro_RO")
    headers = [
        "person_name", "user_name", "email", "personal_number", "birth_date",
        "address", "phone", "mac_address", "ip_address", "iban", "accessed_at",
        "session_duration", "download_speed", "upload_speed", "consumed_traffic"
    ]

    with open(file_path, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for _ in range(rows):
            writer.writerow(generate_record(fake))
    
    logging.info(f"{rows} registros generados en {file_path}")

def add_id(file_path: str) -> None:
    """Agrega una columna de UUID únicos al CSV."""
    df = pl.read_csv(file_path)
    uuid_list = [str(uuid.uuid4()) for _ in range(df.height)]
    df = df.with_columns(pl.Series("unique_id", uuid_list))
    df.write_csv(file_path)
    logging.info("Se agregó columna de UUIDs.")

def update_datetime(file_path: str, mode: str = "next") -> None:
    """Actualiza el campo 'accessed_at' a la fecha de ayer (modo 'next')."""
    if mode == "next":
        current_time = datetime.now().replace(microsecond=0)
        yesterday = str(current_time - timedelta(days=1))
        df = pl.read_csv(file_path)
        df = df.with_columns(pl.lit(yesterday).alias("accessed_at"))
        df.write_csv(file_path)
        logging.info("Campo 'accessed_at' actualizado a la fecha de ayer.")

# 👇 Punto de entrada
if __name__ == "__main__":
    output_file = "data_2/bronze/historical_data.csv"
    registros = 100  # Puedes cambiar esta cantidad si deseas más o menos

    write_to_csv(output_file, registros)
    add_id(output_file)
    # update_datetime(output_file, "next")  # Descomenta si quieres usar fecha de ayer
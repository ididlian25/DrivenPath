from faker import Faker
import polars as pl
from datetime import datetime
import random
import os

fake = Faker()

def save_raw_data():
    records = []
    for _ in range(100):
        records.append({
            "person_name": fake.name(),
            "user_name": fake.user_name(),
            "email": fake.email(),
            "personal_number": fake.random_number(digits=10),
            "birth_date": fake.date_of_birth().isoformat(),
            "address": fake.address().replace("\n", ", "),
            "phone": fake.phone_number(),
            "mac_address": fake.mac_address(),
            "ip_address": fake.ipv4(),
            "iban": fake.iban(),
            "accessed_at": datetime.now(),
            "session_duration": random.randint(30, 3000),
            "download_speed": random.randint(10, 100),
            "upload_speed": random.randint(5, 50),
            "consumed_traffic": random.randint(100, 10000),
            "unique_id": fake.uuid4()
        })

    df = pl.DataFrame(records)

    output_path = '/opt/airflow/data/raw_data.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.write_csv(output_path)

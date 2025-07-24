import polars as pl
import logging
import os

# Configurar el logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def split_into_tables(input_path: str, output_dir: str) -> None:
    """Lee los datos de Silver y los divide en tablas Golden."""

    logging.info("📥 Cargando datos desde Silver...")
    df = pl.read_csv(input_path)

    logging.info("🔍 Separando columnas por tema...")

    financial_cols = ["unique_id", "iban"]
    technical_cols = ["unique_id", "session_duration", "download_speed", "upload_speed", "consumed_traffic"]
    pii_cols = ["unique_id", "mac_address", "ip_address", "accessed_at"]
    non_pii_cols = ["unique_id", "mac_address", "ip_address", "accessed_at"]

    tables = {
        "financial.csv": financial_cols,
        "technical.csv": technical_cols,
        "pii.csv": pii_cols,
        "non_pii.csv": non_pii_cols
    }

    os.makedirs(output_dir, exist_ok=True)

    for filename, columns in tables.items():
        table_df = df.select(columns)
        output_path = os.path.join(output_dir, filename)
        table_df.write_csv(output_path)
        logging.info(f"💾 Guardado: {filename}")
if __name__ == "__main__":
    print("💛 Ejecutando separación Golden...")
    input_path = "data_2/silver/transformed_data.csv"
    output_dir = "data_2/golden"
    split_into_tables(input_path, output_dir)
    logging.info("✨ ¡Capa Golden generada con éxito!")
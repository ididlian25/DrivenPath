import polars as pl
import logging

# Configurar el logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def transform_data(input_path: str, output_path: str) -> None:
    """Lee los datos desde Bronze, aplica transformaciones y guarda en Silver."""
    logging.info("Cargando datos desde Bronze...")
    df = pl.read_csv(input_path)

    logging.info("Aplicando transformaciones...")

    # Convertir columnas a tipo correcto
    df = df.with_columns([
        pl.col("birth_date").str.strptime(pl.Date, "%Y-%m-%d", strict=False),
        pl.col("accessed_at").str.strptime(pl.Datetime, "%Y-%m-%d %H:%M:%S", strict=False),
        pl.col("session_duration").cast(pl.Int32),
        pl.col("download_speed").cast(pl.Int32),
        pl.col("upload_speed").cast(pl.Int32),
        pl.col("consumed_traffic").cast(pl.Int32)
    ])

    logging.info("Guardando datos transformados en Silver...")
    df.write_csv(output_path)

    logging.info("Transformación completada con éxito.")
if __name__ == "__main__":
    print("💡 Ejecutando transformación Silver...")
    input_file = "data_2/bronze/historical_data.csv"
    output_file = "data_2/silver/transformed_data.csv"
    transform_data(input_file, output_file)
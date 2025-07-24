import polars as pl
import logging
import os

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

# Directorio donde están tus .csv Golden
golden_dir = "data_2/golden"

# Cargar cada tabla
logging.info("📥 Leyendo archivos Golden...")
financial = pl.read_csv(os.path.join(golden_dir, "financial.csv"))
technical = pl.read_csv(os.path.join(golden_dir, "technical.csv"))
pii = pl.read_csv(os.path.join(golden_dir, "pii.csv"))
non_pii = pl.read_csv(os.path.join(golden_dir, "non_pii.csv"))

# Combinar todas por 'unique_id'
logging.info("🧬 Fusionando tablas...")
final_df = pii.join(financial, on="unique_id", how="inner") \
              .join(technical, on="unique_id", how="inner") \
              .join(non_pii, on="unique_id", how="inner")

# Guardar el archivo combinado
output_path = os.path.join(golden_dir, "golden_unified.csv")
final_df.write_csv(output_path)
logging.info(f"✅ Archivo unificado guardado en: {output_path}")
# Eliminar columnas "_right" para evitar duplicados
final_df = final_df.drop(["mac_address_right", "ip_address_right", "accessed_at_right"])
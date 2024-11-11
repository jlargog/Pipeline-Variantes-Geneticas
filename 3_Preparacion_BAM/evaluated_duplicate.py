import os
import pandas as pd
import re

# Define el directorio de métricas
metrics_dir = "/datos/home/johanlargo/proyectos/20240509-dcl/1_bam_files/4_marked_duplicates"

# Lista para almacenar los datos de cada archivo
data = []

# Expresión regular para extraer el nombre de la muestra (DCL_XXX)
sample_pattern = re.compile(r"marked_dup_metrics_(DCL_\d+)_")

# Recorrer cada archivo en el directorio
for file in os.listdir(metrics_dir):
    if file.startswith("marked_dup_metrics") and file.endswith(".txt"):
        file_path = os.path.join(metrics_dir, file)
        
        # Extraer el nombre de la muestra usando la expresión regular
        sample_match = sample_pattern.search(file)
        sample_name = sample_match.group(1) if sample_match else "Unknown"

        # Abrir y leer el archivo de métricas
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        # Extraer los valores específicos
        metrics = {}
        for line in lines:
            if line.startswith("LIBRARY"):
                headers = line.strip().split()
            elif "mgi_library" in line:
                values = line.strip().split()
                metrics = dict(zip(headers, values))
        
        # Convertir los valores numéricos y agregar el nombre del archivo y de la muestra
        metrics = {k: float(v) if k not in ['LIBRARY'] else v for k, v in metrics.items()}
        metrics['FILENAME'] = file  # Añadir el nombre del archivo para identificar cada muestra
        metrics['SAMPLE'] = sample_name  # Añadir el nombre de la muestra extraído

        # Añadir los datos de este archivo a la lista
        data.append(metrics)

# Crear un DataFrame con todos los datos
df = pd.DataFrame(data)

# Seleccionar las columnas relevantes para el análisis
df = df[['FILENAME', 'SAMPLE', 'UNPAIRED_READS_EXAMINED', 'READ_PAIRS_EXAMINED', 
         'UNPAIRED_READ_DUPLICATES', 'READ_PAIR_DUPLICATES', 'PERCENT_DUPLICATION', 
         'ESTIMATED_LIBRARY_SIZE']]

# Guardar el DataFrame en un archivo CSV para un análisis posterior o visualización
df.to_csv("consolidated_duplication_metrics.csv", index=False)

# Mostrar los primeros resultados
print(df.head())






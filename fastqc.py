import os
import subprocess

# Ruta de la carpeta de entrada y salida
carpeta_entrada = "/datos/home/johanlargo/proyectos/20230703-alzheimer/0_rawdata/data"
carpeta_salida = "/datos/home/johanlargo/proyectos/20230703-alzheimer/1_quality_visual"

# Obtener la lista de subcarpetas en la carpeta de entrada
subcarpetas = os.listdir(carpeta_entrada)

# Recorrer cada subcarpeta
for subcarpeta in subcarpetas:
    # Construir la ruta completa de la subcarpeta
    ruta_subcarpeta = os.path.join(carpeta_entrada, subcarpeta)

    # Verificar que la subcarpeta sea un directorio
    if os.path.isdir(ruta_subcarpeta):
        # Obtener la lista de archivos .fastq.gz en la subcarpeta
        archivos_fastq = [
            archivo for archivo in os.listdir(ruta_subcarpeta) if archivo.endswith(".fastq.gz")
        ]

        # Crear la carpeta de salida para la subcarpeta actual
        ruta_carpeta_salida = os.path.join(carpeta_salida, subcarpeta)
        os.makedirs(ruta_carpeta_salida, exist_ok=True)

        # Ejecutar FastQC para cada archivo .fastq.gz
        for archivo_fastq in archivos_fastq:
            # Construir la ruta completa del archivo de entrada
            ruta_archivo_entrada = os.path.join(ruta_subcarpeta, archivo_fastq)

            # Construir el nombre del archivo de salida basado en el nombre original
            nombre_archivo_salida = archivo_fastq.replace(".fastq.gz", "_fastqc.html")
            ruta_archivo_salida = os.path.join(ruta_carpeta_salida, nombre_archivo_salida)

            # Ejecutar FastQC en el archivo de entrada
            subprocess.run(["fastqc", ruta_archivo_entrada, "-o", ruta_carpeta_salida])

            # Renombrar el archivo de salida de FastQC para reflejar el nombre original del archivo fastq.gz
            nuevo_nombre_archivo_salida = archivo_fastq.replace(".fastq.gz", "_fastqc.html")
            ruta_nuevo_archivo_salida = os.path.join(ruta_carpeta_salida, nuevo_nombre_archivo_salida)
            os.rename(ruta_archivo_salida, ruta_nuevo_archivo_salida)

            print(f"Se completó el análisis para {archivo_fastq} en {ruta_carpeta_salida}")


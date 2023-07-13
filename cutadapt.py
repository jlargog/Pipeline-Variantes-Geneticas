import os
import subprocess

# Ruta de la carpeta de entrada y salida
carpeta_entrada = "/datos/home/johanlargo/proyectos/20230703-alzheimer/0_rawdata/data"
carpeta_salida = "/datos/home/johanlargo/proyectos/20230703-alzheimer/2_quality_trimming"

# Obtener la lista de subcarpetas en la carpeta de entrada
subcarpetas = os.listdir(carpeta_entrada)

# Recorrer cada subcarpeta
for subcarpeta in subcarpetas:
    # Construir la ruta completa de la subcarpeta
    ruta_subcarpeta = os.path.join(carpeta_entrada, subcarpeta)

    # Verificar que la subcarpeta sea un directorio
    if os.path.isdir(ruta_subcarpeta):
        # Obtener la lista de archivos _R1.fastq.gz en la subcarpeta
        archivos_forward = [
            archivo for archivo in os.listdir(ruta_subcarpeta) if archivo.endswith("_R1.fastq.gz")
        ]

        # Crear la carpeta de salida para la subcarpeta actual
        ruta_carpeta_salida = os.path.join(carpeta_salida, subcarpeta)
        os.makedirs(ruta_carpeta_salida, exist_ok=True)

        # Ejecutar Cutadapt para cada archivo forward (_R1.fastq.gz)
        for archivo_forward in archivos_forward:
            # Construir la ruta completa del archivo forward
            ruta_archivo_forward = os.path.join(ruta_subcarpeta, archivo_forward)

            # Construir el nombre del archivo de salida basado en el nombre original
            nombre_archivo_salida_forward = archivo_forward.replace("_R1.fastq.gz", "_fastqc.gz")
            ruta_archivo_salida_forward = os.path.join(ruta_carpeta_salida, nombre_archivo_salida_forward)

            # Ejecutar Cutadapt en el archivo forward
            subprocess.run([
                "cutadapt",
                "-j", "20",
                "-a", "ATCGGAAGAGCACACGTCTGAACTCCAGTCACCGGCTATGATCTCGTATG",
                "--poly-a",
                "-g", "GGGGGG",
                "--trim-n",
                "-m", "151",
                "-q", "21",
                "-o", ruta_archivo_salida_forward,
                ruta_archivo_forward
            ])

            print(f"Se completó el análisis para {archivo_forward} en {ruta_carpeta_salida}")

        # Obtener la lista de archivos _R2.fastq.gz en la subcarpeta
        archivos_reverse = [
            archivo for archivo in os.listdir(ruta_subcarpeta) if archivo.endswith("_R2.fastq.gz")
        ]

        # Ejecutar Cutadapt para cada archivo reverse (_R2.fastq.gz)
        for archivo_reverse in archivos_reverse:
            # Construir la ruta completa del archivo reverse
            ruta_archivo_reverse = os.path.join(ruta_subcarpeta, archivo_reverse)

            # Construir el nombre del archivo de salida basado en el nombre original
            nombre_archivo_salida_reverse = archivo_reverse.replace("_R2.fastq.gz", "_fastqc.gz")
            ruta_archivo_salida_reverse = os.path.join(ruta_carpeta_salida, nombre_archivo_salida_reverse)

            # Ejecutar Cutadapt en el archivo reverse
            subprocess.run([
                "cutadapt",
                "-j", "20",
                "-a", "ATCGGAAGAGCACACGTCTGAACTCCAGTCACCGGCTATGATCTCGTATG",
                "--poly-a",
                "-g", "GGGGGG",
                "--trim-n",
                "-m", "151",
                "-q", "21",
                "-o", ruta_archivo_salida_reverse,
                ruta_archivo_reverse
            ])

            print(f"Se completó el análisis para {archivo_reverse} en {ruta_carpeta_salida}")


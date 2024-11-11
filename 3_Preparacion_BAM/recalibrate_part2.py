import os
import subprocess

# Configurar el entorno específico
os.environ['PATH'] = '/datos/home/johanlargo/aplicaciones/anaconda3/envs/gwas/bin:' + os.environ['PATH']

# Definir las rutas absolutas y directorios
input_dir = "/datos/home/johanlargo/proyectos/20240509-dcl/1_bam_files/4_marked_duplicates"
output_dir = "/datos/home/johanlargo/proyectos/20240509-dcl/1_bam_files/5_recalibrate"
reference_genome = "/datos/home/johanlargo/proyectos/20240509-dcl/gatk_resources/reference_genome/Homo_sapiens_assembly38.fasta"

# Definir la ruta al directorio donde se encuentran los archivos de recalibración
recall_tables_dir = "/datos/home/johanlargo/proyectos/20240509-dcl/1_bam_files/5_recalibrate"

# Crear el directorio de salida si no existe
os.makedirs(output_dir, exist_ok=True)

# Obtener la lista de archivos BAM en el directorio de entrada
bam_files = [f for f in os.listdir(input_dir) if f.endswith('.bam')]

# Iterar sobre cada archivo BAM y ejecutar GATK ApplyBQSR
for bam_file in bam_files:
    sample_name = bam_file.split('.')[0]  # Obtener el nombre del archivo sin la extensión
    input_bam = os.path.join(input_dir, bam_file)
    recal_file = os.path.join(recall_tables_dir, f"{sample_name}.table")
    output_bam = os.path.join(output_dir, f"{sample_name}.sort.dup.bqsr.bam")

    # Comando GATK ApplyBQSR
    gatk_command = [
        "gatk",
        "--java-options", "-Xmx20g -Dtica.numberOfThreads=40",
        "ApplyBQSR",
        "-I", input_bam,
        "-R", reference_genome,
        "--bqsr-recal-file", recal_file,
        "-O", output_bam
    ]

    # Ejecutar el comando y capturar la salida
    process = subprocess.Popen(gatk_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    # Decodificar la salida y los errores en formato UTF-8
    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')

    # Escribir la salida y los errores en nohup.out
    with open("nohup.out", "a") as nohup_file:
        nohup_file.write(stdout)
        nohup_file.write(stderr)

    # Imprimir un mensaje para verificar el progreso
    print(f"Procesado {bam_file}")

print("Recalibración completada.")


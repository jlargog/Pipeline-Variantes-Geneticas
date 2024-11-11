import os
import subprocess

# Configurar el entorno específico
os.environ['PATH'] = '/datos/home/johanlargo/aplicaciones/anaconda3/envs/gwas/bin:' + os.environ['PATH']

# Definir las rutas absolutas y directorios
input_dir = "/datos/home/johanlargo/proyectos/20240509-dcl/1_bam_files/4_marked_duplicates"
output_dir = "/datos/home/johanlargo/proyectos/20240509-dcl/1_bam_files/5_recalibrate"
reference_genome = "/datos/home/johanlargo/proyectos/20240509-dcl/gatk_resources/reference_genome/Homo_sapiens_assembly38.fasta"
known_sites = "/datos/home/johanlargo/proyectos/20240509-dcl/gatk_resources/Homo_sapiens_assembly38.dbsnp138.vcf"
reference_dict = "/datos/home/johanlargo/proyectos/20240509-dcl/gatk_resources/reference_genome/Homo_sapiens_assembly38.dict"

# Generar diccionario de secuencia si no existe
if not os.path.exists(reference_dict):
    subprocess.run(["java", "-jar", "picard.jar", "CreateSequenceDictionary",
                    "R=" + reference_genome,
                    "O=" + reference_dict])

# Obtener la lista de archivos BAM en el directorio de entrada
bam_files = [f for f in os.listdir(input_dir) if f.endswith('.bam')]

# Crear el directorio de salida si no existe
os.makedirs(output_dir, exist_ok=True)

# Iterar sobre cada archivo BAM y ejecutar GATK BaseRecalibrator
for bam_file in bam_files:
    sample_name = bam_file.split('.')[0]  # Obtener el nombre del archivo sin la extensión
    input_bam = os.path.join(input_dir, bam_file)
    output_table = os.path.join(output_dir, f"{sample_name}.table")

    # Comando GATK BaseRecalibrator
    gatk_command = [
        "gatk",
        "--java-options", "-Xmx20g -Dtica.numberOfThreads=40 -DGATK_STACKTRACE_ON_USER_EXCEPTION=true",
        "BaseRecalibrator",
        "-I", input_bam,
        "-R", reference_genome,
        "--known-sites", known_sites,
        "-O", output_table
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


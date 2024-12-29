import os
import subprocess

# Directorios y archivo de referencia
input_dir = "/datos/home/johanlargo/proyectos/20240509-dcl/1_bam_files/5_recalibrate"
output_dir = "/datos/home/johanlargo/proyectos/20240509-dcl/2_vcf_files/1_only_vcf"
reference_genome = "/datos/home/johanlargo/proyectos/20240509-dcl/gatk_resources/reference_genome/Homo_sapiens_assembly38.fasta"

# Crear el directorio de salida si no existe
os.makedirs(output_dir, exist_ok=True)

# Función para ejecutar el comando GATK HaplotypeCaller
def run_gatk_haplotypecaller(bam_file, output_file):
    command = [
        "/datos/home/johanlargo/aplicaciones/anaconda3/envs/gwas/bin/gatk",
        "--java-options", "-Xmx10g -Dtica.numberOfThreads=40",
        "HaplotypeCaller",
        "-I", bam_file,
        "-R", reference_genome,
        "-ERC", "GVCF",
        "-O", output_file
    ]
    subprocess.run(command, check=True)

# Procesar cada archivo .bam en el directorio de entrada
for bam_file in os.listdir(input_dir):
    if bam_file.endswith(".bam"):
        input_path = os.path.join(input_dir, bam_file)
        filename = os.path.splitext(bam_file)[0]
        output_path = os.path.join(output_dir, f"{filename}.vcf.gz")
        
        print(f"Processing {bam_file}...")
        run_gatk_haplotypecaller(input_path, output_path)

print("Todos los trabajos de HaplotypeCaller han sido iniciados.")


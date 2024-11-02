import os
import subprocess
import shutil

def alinear_con_bwa(ruta_genoma_referencia, carpeta_fastq, carpeta_salida, archivo_registro):
    archivos_fastq = [f for f in os.listdir(carpeta_fastq) if f.endswith('.fastq.gz')]

    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    ruta_registro = os.path.join(carpeta_salida, archivo_registro)

    with open(ruta_registro, 'w') as registro:
        for i in range(0, len(archivos_fastq), 2):
            archivo_fastq_1 = archivos_fastq[i]
            archivo_fastq_2 = archivos_fastq[i + 1]

            ruta_fastq_1 = os.path.join(carpeta_fastq, archivo_fastq_1)
            ruta_fastq_2 = os.path.join(carpeta_fastq, archivo_fastq_2)

            nombre_archivo_sam = archivo_fastq_1.replace('_1.fastq.gz', '.sam')
            ruta_salida_sam = os.path.join(carpeta_salida, nombre_archivo_sam)

            comando_bwa = ['bwa', 'mem', '-t', '40', ruta_genoma_referencia, ruta_fastq_1, ruta_fastq_2]

            with open(ruta_salida_sam, 'w') as archivo_salida_sam:
                subprocess.run(comando_bwa, stdout=archivo_salida_sam)

            nombre_archivo_bam = nombre_archivo_sam.replace('.sam', '.bam')
            ruta_salida_bam = os.path.join(carpeta_salida, nombre_archivo_bam)
            # Convertir SAM a BAM
            comando_samtools = ['samtools', 'view', '-@', '40', '-bS', ruta_salida_sam, '-o', ruta_salida_bam]
            subprocess.run(comando_samtools)

            # Eliminar archivos SAM
            os.remove(ruta_salida_sam)

            registro.write(f"Archivos {archivo_fastq_1} y {archivo_fastq_2}: \n")

    return ruta_registro

# Rutas a los archivos y carpetas
ruta_genoma_referencia = '/datos/home/johanlargo/proyectos/20240509-dcl/gatk_resources/reference_genome/Homo_sapiens_assembly38.fasta'
carpeta_fastq = '/datos/home/johanlargo/DatosDCL'
carpeta_salida = '/datos/home/johanlargo/proyectos/20240509-dcl/1_bam_files/1_alignment'
archivo_registro = 'registro.txt'

# Almacenar ruta de registro
ruta_registro = alinear_con_bwa(ruta_genoma_referencia, carpeta_fastq, carpeta_salida, archivo_registro)


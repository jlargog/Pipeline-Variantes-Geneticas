import os
import subprocess
import shlex

# Directorio de entrada de los archivos BAM ordenados
sorted_bam_dir = "/datos/home/johanlargo/proyectos/20240509-dcl/1_bam_files/3_sort"

# Directorio de salida para los archivos BAM con duplicados marcados
marked_dup_dir = "/datos/home/johanlargo/proyectos/20240509-dcl/1_bam_files/4_marked_duplicates"

# Comando para marcar duplicados
command_mark_duplicates = """
java -Djava.io.tmpdir=/datos/home/johanlargo/tmp -Xmx10g -jar /datos/home/johanlargo/aplicaciones/anaconda3/envs/gwas/share/picard-2.27.5-0/picard.jar MarkDuplicates \
I={input_file} \
O={output_file} \
METRICS_FILE={metrics_file} \
"""

# Asegurarse de que el directorio de salida existe
os.makedirs(marked_dup_dir, exist_ok=True)

# Iterar sobre los archivos BAM ordenados en el directorio de entrada
for file in os.listdir(sorted_bam_dir):
    if file.endswith(".rg.sorted.bam"):
        input_file = os.path.join(sorted_bam_dir, file)
        output_file = os.path.join(marked_dup_dir, file.replace(".rg.sorted.bam", ".marked_dup.bam"))
        metrics_file = os.path.join(marked_dup_dir, "marked_dup_metrics_" + file.replace(".rg.sorted.bam", ".txt"))

        # Formatear el comando con los archivos de entrada y salida
        command = command_mark_duplicates.format(input_file=input_file, output_file=output_file, metrics_file=metrics_file)

        # Dividir el comando en una lista de argumentos
        args = shlex.split(command)

        try:
            # Ejecutar el comando
            print(f"Procesando archivo: {file}")
            result = subprocess.run(args, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"Archivo procesado correctamente: {file}")
        except subprocess.CalledProcessError as e:
            print(f"Error procesando {file}: {e.stderr.decode('utf-8')}")

print("Todos los archivos han sido procesados.")


import os
import subprocess
import shlex

# Directorio de entrada
input_dir = "/datos/home/johanlargo/proyectos/20240509-dcl/1_bam_files/2_read_group"

# Directorio de salida
output_dir = "/datos/home/johanlargo/proyectos/20240509-dcl/1_bam_files/3_sort"

# Comando base
command_template = """
java -Djava.io.tmpdir=/datos/home/johanlargo/tmp -Xmx100g -jar /datos/home/johanlargo/aplicaciones/anaconda3/envs/gwas/share/picard-2.27.5-0/picard.jar SortSam \
I={input_file} \
O={output_file} \
VALIDATION_STRINGENCY=LENIENT \
SORT_ORDER=coordinate \
MAX_RECORDS_IN_RAM=3000000 \
CREATE_INDEX=True
"""

# Asegurarse de que el directorio de salida existe
os.makedirs(output_dir, exist_ok=True)

# Iterar sobre los archivos DCL_* en el directorio de entrada
for file in os.listdir(input_dir):
    if file.startswith("DCL_"):
        input_file = os.path.join(input_dir, file)
        output_file = os.path.join(output_dir, file + ".rg.sorted.bam")

        # Formatear el comando con los archivos de entrada y salida
        command = command_template.format(input_file=input_file, output_file=output_file)

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


import os
import subprocess

# Define el directorio que contiene los archivos BAM
bam_directory = '/datos/home/johanlargo/proyectos/20240509-dcl/1_bam_files/1_alignment'
gatk_path = '/datos/home/johanlargo/aplicaciones/anaconda3/envs/gwas/bin/gatk'
output_directory = '/datos/home/johanlargo/proyectos/20240509-dcl/1_bam_files/2_read_group'
java_options = '-Xmx50g'

# Asegúrate de que el directorio de salida exista
os.makedirs(output_directory, exist_ok=True)

# Define la función para generar y ejecutar el comando GATK
def process_bam_file(bam_file):
    bam_file_path = os.path.join(bam_directory, bam_file)
    
    # Extrae información del nombre del archivo BAM
    parts = bam_file.split('_')
    sample_id = parts[0] + '_' + parts[1]
    rgid = bam_file.split('.')[0]
    
    # Construye el nombre del archivo de salida
    output_bam_file = os.path.join(output_directory, bam_file.replace('.bam', '.rg.bam'))
    
    # Construye el comando GATK
    gatk_command = [
        gatk_path, '--java-options', java_options, 'AddOrReplaceReadGroups',
        '-I', bam_file_path,
        '-O', output_bam_file,
        '--RGID', rgid,
        '--RGLB', 'mgi_library',
        '--RGPL', 'MGI',
        '--RGPU', rgid,
        '--RGSM', sample_id
    ]
    
    # Ejecuta el comando GATK y verifica si se ejecuta correctamente
    try:
        result = subprocess.run(gatk_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Processed {bam_file}: {result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error processing {bam_file}: {e.stderr}")
        # Elimina el archivo de salida si no se generó correctamente
        if os.path.exists(output_bam_file):
            os.remove(output_bam_file)

# Obtiene la lista de archivos BAM en el directorio
bam_files = [f for f in os.listdir(bam_directory) if f.endswith('.bam')]

# Procesa cada archivo BAM
for bam_file in bam_files:
    process_bam_file(bam_file)


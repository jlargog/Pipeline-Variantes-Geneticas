# Alineamiento al Genoma de Referencia

En esta sección se realizó el alineamiento al genoma de referencia y se desarrolló un script en Python que permite generar los diferentes archivos `.BAM`. El script se denomina `alignment.py` y está disponible en este repositorio para su visualización y descarga. Este script automatiza el proceso de alineación de secuencias FASTQ utilizando la herramienta **BWA** (Burrows-Wheeler Aligner) y convierte los archivos resultantes a formato BAM usando **Samtools**.

## Detalles del Script

A continuación, se detallan los programas y las opciones empleadas:

### Programas utilizados

#### BWA
- **Comando**: Se usa el comando `bwa mem` para alinear las secuencias FASTQ a un genoma de referencia.
- **Opciones**:
  - `-t 40`: Utiliza 40 hilos para el procesamiento paralelo.
  - `ruta_genoma_referencia`: Ruta al genoma de referencia (en formato `.fasta`).
  - `ruta_fastq_1` y `ruta_fastq_2`: Archivos FASTQ de lectura (pares).

#### Samtools
- Después de generar los archivos `.sam` con BWA, se utiliza `samtools view` para convertir los archivos SAM a BAM.
- **Opciones**:
  - `-@ 40`: Usa 40 hilos para acelerar la conversión.
  - `-bS`: Especifica la conversión de SAM a BAM.
  - `-o`: Especifica el archivo de salida en formato `.bam`.

Este enfoque permite una gestión eficiente del alineamiento y conversión de datos, facilitando el análisis posterior de las secuencias alineadas.

Para este proceso se diseño un script denominado run_gatk_haplotypecaller.py Este script automatiza el proceso de llamado de variantes (variant calling) a partir de archivos BAM utilizando la herramienta GATK HaplotypeCaller. Este análisis es un paso clave en estudios genómicos para identificar variantes genéticas (como SNPs o indels) a partir de lecturas alineadas. Este script genero los diferenrtes archivos vcf se generró un script denominado generate_vcf_stats.sh que permite guardar un resumen de las stats de cada archivo. 

Función principal:

Ejecuta GATK HaplotypeCaller para procesar cada archivo BAM.
Genera archivos VCF comprimidos (.vcf.gz) con las variantes detectadas.
Usa 10 GB de memoria y 40 hilos para optimizar el rendimiento.
Iteración sobre BAMs:

Procesa todos los archivos BAM del directorio de entrada.
Llama a la función para ejecutar el análisis y genera los archivos VCF correspondientes.
Mensajes de progreso: Imprime el estado del procesamiento para cada archivo.

Características clave:

Automatiza el análisis de múltiples BAMs.
Escalable, eficiente y adaptable para grandes volúmenes de datos.
Genera salidas en formato estándar (.vcf.gz).
Detalles de GATK HaplotypeCaller:

Identifica variantes genéticas (SNPs e indels) usando un genoma de referencia.
Genera GVCFs para análisis conjunto.

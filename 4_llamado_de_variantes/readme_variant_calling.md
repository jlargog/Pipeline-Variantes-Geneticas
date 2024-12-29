# Generación de un archivo VCF de alta calidad

El objetivo de este capítulo es la generación de un archivo VCF que cumpla con las condiciones de calidad necesarias para realizar análisis como **GWAS (Genome-Wide Association Studies)**, análisis de ancestría y comparación de SNPs entre casos y controles. Para lograrlo, se han desarrollado y ejecutado las siguientes secciones:

## Llamado de variantes

Se diseñó un script denominado [`run_gatk_haplotypecaller.py`](run_gatk_haplotypecaller.py), que automatiza el proceso de llamado de variantes (*variant calling*) a partir de archivos BAM utilizando la herramienta **GATK HaplotypeCaller**. Este análisis es esencial en estudios genómicos para identificar variantes genéticas, como SNPs e indels, a partir de lecturas alineadas.

### Funcionalidades principales del script:
- Ejecuta **GATK HaplotypeCaller** para procesar cada archivo BAM.
- Genera archivos VCF comprimidos (`.vcf.gz`) con las variantes detectadas.
- Usa 10 GB de memoria y 40 hilos para optimizar el rendimiento.

### Detalles adicionales:
- Procesa automáticamente todos los archivos BAM del directorio de entrada.
- Imprime mensajes de progreso para cada archivo procesado.
- Escalable, eficiente y adaptable para grandes volúmenes de datos.
- Genera salidas en formato estándar (`.vcf.gz`) compatibles con análisis posteriores.

Además, se creó el script [`generate_vcf_stats.sh`](generate_vcf_stats.sh), que permite generar un resumen de las estadísticas de cada archivo VCF.

## Combinación de múltiples VCF en uno solo

Se ejeucto un [`comando`](combinarGVCFs.txt) que utiliza **GATK CombineGVCFs** para combinar múltiples archivos VCF comprimidos (`.vcf.gz`) en un único archivo denominado `cohort.g.vcf.gz`. Este paso permite consolidar todas las variantes detectadas en diferentes muestras para su análisis conjunto posterior, como el llamado de variantes en cohortes.

- Se utilizó el genoma de referencia `Homo_sapiens_assembly38.fasta`.
- Se asignaron 100 GB de memoria y 40 hilos para optimizar el rendimiento.
- Se ejecutó el proceso en segundo plano con `nohup`.

## Genotipado del archivo combinado

Se realizó el genotipado del archivo combinado `cohort.g.vcf.gz` mediante **GATK GenotypeGVCFs**, generando el archivo `output.vcf.gz`, que contiene las variantes genotipadas. Posteriormente, se llevó a cabo el recalibrado de variantes en dos pasos:

1. **VariantRecalibrator**: Construyó un modelo de calidad para los SNPs usando recursos de referencia conocidos.
2. **ApplyVQSR**: Filtró variantes según el modelo, obteniendo como salida el archivo filtrado `cohort_snps_filtered.vcf.gz`.

Ambos pasos se ejecutaron en segundo plano con `nohup`.

## Filtrado de variantes

Se realizó el filtrado de variantes en el archivo recalibrado `cohort_snps_filtered.vcf.gz` utilizando **GATK VariantFiltration**, aplicando umbrales específicos de calidad, como:
- **Profundidad de lectura (DP)**: Variantes con DP < 10 se marcaron como de baja calidad.
- **Calidad de mapeo (MQ)**: Variantes con MQ < 40.0 se filtraron.
- **Otras métricas**: SOR > 3.0, FS > 60.0, MQRankSum < -12.5 y ReadPosRankSum < -8.0.

Las variantes que pasaron los filtros se extrajeron con **bcftools** y se guardaron en el archivo `cohort_final_filtered.vqsr.varfilter.pass.vcf`. Este archivo fue comprimido con **bgzip** y se generó un índice con **bcftools index**, obteniendo el archivo final comprimido e indexado `cohort_final_filtered.vqsr.varfilter.pass.vcf.gz`, listo para su uso en análisis posteriores.


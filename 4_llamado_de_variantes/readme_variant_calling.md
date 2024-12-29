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

Se ejeucto un [`comando`](comandoCombineGVCFs.txt) que utiliza **GATK CombineGVCFs** para combinar múltiples archivos VCF comprimidos (`.vcf.gz`) en un único archivo denominado `cohort.g.vcf.gz`. Este paso permite consolidar todas las variantes detectadas en diferentes muestras para su análisis conjunto posterior, como el llamado de variantes en cohortes.

- Se utilizó el genoma de referencia `Homo_sapiens_assembly38.fasta`.
- Se asignaron 100 GB de memoria y 40 hilos para optimizar el rendimiento.
- Se ejecutó el proceso en segundo plano con `nohup`.

## Genotipado del archivo combinado

Se realizó el genotipado del archivo combinado `cohort.g.vcf.gz` mediante **GATK GenotypeGVCFs**, generando el archivo `output.vcf.gz`, que contiene las variantes genotipadas:

```bash
nohup /datos/home/johanlargo/aplicaciones/anaconda3/envs/gwas/bin/gatk --java-options "-Xmx40g -Dtica.numberOfThreads=40" GenotypeGVCFs \
    -R /datos/home/johanlargo/proyectos/20240509-dcl/gatk_resources/reference_genome/Homo_sapiens_assembly38.fasta \
    -V /datos/home/johanlargo/proyectos/20240509-dcl/2_vcf_files/1_only_vcf/cohort.g.vcf.gz \
    -O /datos/home/johanlargo/proyectos/20240509-dcl/2_vcf_files/3_combine_all_vcf/output.vcf.gz &```


Posteriormente, se llevó a cabo el recalibrado de variantes en dos pasos:

1. **VariantRecalibrator**: Construyó un modelo de calidad para los SNPs usando recursos de referencia conocidos.
## GATK VariantRecalibrator

El comando ejecuta **GATK VariantRecalibrator**, una herramienta que construye un modelo de calidad para las variantes identificadas (en este caso, SNPs) utilizando recursos de referencia conocidos y varias métricas de calidad. 

### Qué hace este comando

- **Entrada del archivo VCF**: Toma el archivo de variantes genotipadas `output.vcf.gz` generado previamente.
- **Modo de recalibrado**: Se especifica `-mode SNP`, lo que indica que el recalibrado será aplicado exclusivamente a los SNPs.
- **Recursos de referencia**:
  - `hapmap`, `omni`, `1000G`, y `dbsnp` son bases de datos de alta confianza que proporcionan variantes conocidas para el entrenamiento del modelo.
  - Cada recurso incluye atributos como:
    - **`known`**: Si es un recurso conocido.
    - **`training`**: Si es utilizado para entrenamiento del modelo.
    - **`truth`**: Si es utilizado como verdad para evaluar el modelo.
    - **`prior`**: Peso asignado al recurso.
- **Métricas analizadas (`-an`)**:
  - `QD`: Calidad por profundidad.
  - `MQRankSum`: Sesgo en la calidad de mapeo entre las lecturas de referencia y las alternativas.
  - `ReadPosRankSum`: Sesgo en la posición de lectura de variantes alternativas frente a la referencia.
  - `FS`: Valor de Fisher Strand para detectar sesgos en la cadena.
  - `MQ`: Calidad promedio de mapeo.
  - `SOR`: Relación de sesgo de la cadena.
  - `DP`: Profundidad de lectura.
- **Salida**:
  - Archivo `cohort_snps.recal`: Contiene el modelo de recalibrado para los SNPs.
  - Archivo `cohort_snps.tranches`: Muestra los rangos de calidad y los umbrales generados.
- **Recursos asignados**:
  - Usa 40 GB de memoria (`-Xmx40g`) y 40 hilos (`-Dtica.numberOfThreads=40`) para optimizar el rendimiento.
- **Ejecución en segundo plano**: El comando se ejecuta con `nohup` para que continúe funcionando incluso si se cierra la terminal.



```bash
nohup /datos/home/johanlargo/aplicaciones/anaconda3/envs/gwas/bin/gatk --java-options "-Xmx40g -Dtica.numberOfThreads=40" VariantRecalibrator -V /datos/home/johanlargo/proyectos/20240509-dcl/2_vcf_files/3_combine_all_vcf/output.vcf.gz --trust-all-polymorphic -mode SNP --max-gaussians 6 --resource hapmap,known=false,training=true,truth=true,prior=15:/datos/home/johanlargo/proyectos/20240509-dcl/gatk_resources/hapmap_3.3.hg38.vcf.gz --resource omni,known=false,training=true,truth=true,prior=12:/datos/home/johanlargo/proyectos/20240509-dcl/gatk_resources/1000G_omni2.5.hg38.vcf.gz --resource 1000G,known=false,training=true,truth=false,prior=10:/datos/home/johanlargo/proyectos/20240509-dcl/gatk_resources/1000G_phase1.snps.high_confidence.hg38.vcf.gz --resource dbsnp,known=true,training=false,truth=false,prior=7:/datos/home/johanlargo/proyectos/20240509-dcl/gatk_resources/Homo_sapiens_assembly38.dbsnp138.vcf -an QD -an MQRankSum -an ReadPosRankSum -an FS -an MQ -an SOR -an DP -O /datos/home/johanlargo/proyectos/20240509-dcl/2_vcf_files/3_combine_all_vcf/cohort_snps.recal --tranches-file /datos/home/johanlargo/proyectos/20240509-dcl/2_vcf_files/3_combine_all_vcf/cohort_snps.tranches &

2. **ApplyVQSR**: Filtró variantes según el modelo, obteniendo como salida el archivo filtrado `cohort_snps_filtered.vcf.gz`.

```bash
nohup /datos/home/johanlargo/aplicaciones/anaconda3/envs/gwas/bin/gatk --java-options "-Xmx40g -Dtica.numberOfThreads=40" ApplyVQSR \
    -R /datos/home/johanlargo/proyectos/20240509-dcl/gatk_resources/reference_genome/Homo_sapiens_assembly38.fasta \
    -V /datos/home/johanlargo/proyectos/20240509-dcl/2_vcf_files/3_combine_all_vcf/output.vcf.gz \
    -O /datos/home/johanlargo/proyectos/20240509-dcl/2_vcf_files/3_combine_all_vcf/cohort_snps_filtered.vcf.gz \
    --truth-sensitivity-filter-level 99.0 \
    --tranches-file /datos/home/johanlargo/proyectos/20240509-dcl/2_vcf_files/3_combine_all_vcf/cohort_snps.tranches \
    --recal-file /datos/home/johanlargo/proyectos/20240509-dcl/2_vcf_files/3_combine_all_vcf/cohort_snps.recal \
    -mode SNP &

## Filtrado de variantes

Se realizó el filtrado de variantes en el archivo recalibrado `cohort_snps_filtered.vcf.gz` utilizando **GATK VariantFiltration**, aplicando umbrales específicos de calidad, como:
- **Profundidad de lectura (DP)**: Variantes con DP < 10 se marcaron como de baja calidad.
- **Calidad de mapeo (MQ)**: Variantes con MQ < 40.0 se filtraron.
- **Otras métricas**: SOR > 3.0, FS > 60.0, MQRankSum < -12.5 y ReadPosRankSum < -8.0.

Las variantes que pasaron los filtros se extrajeron con **bcftools** y se guardaron en el archivo `cohort_final_filtered.vqsr.varfilter.pass.vcf`. Este archivo fue comprimido con **bgzip** y se generó un índice con **bcftools index**, obteniendo el archivo final comprimido e indexado `cohort_final_filtered.vqsr.varfilter.pass.vcf.gz`, listo para su uso en análisis posteriores.


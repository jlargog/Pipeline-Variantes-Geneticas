# 4 Generación de un archivo VCF de alta calidad

El objetivo de este capítulo es la generación de un archivo VCF que cumpla con las condiciones de calidad necesarias para realizar análisis como **GWAS (Genome-Wide Association Studies)**, análisis de ancestría y comparación de SNPs entre casos y controles. Para lograrlo, se han desarrollado y ejecutado las siguientes secciones:

## 4.1 Llamado de variantes

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

## 4.2 Combinación de múltiples VCF en uno solo

Se ejeucto un [`comando`](comandoCombineGVCFs.txt) que utiliza **GATK CombineGVCFs** para combinar múltiples archivos VCF comprimidos (`.vcf.gz`) en un único archivo denominado `cohort.g.vcf.gz`. Este paso permite consolidar todas las variantes detectadas en diferentes muestras para su análisis conjunto posterior, como el llamado de variantes en cohortes.

- Se utilizó el genoma de referencia `Homo_sapiens_assembly38.fasta`.
- Se asignaron 100 GB de memoria y 40 hilos para optimizar el rendimiento.
- Se ejecutó el proceso en segundo plano con `nohup`.

## 4.3 Genotipado del archivo combinado

Se realizó el genotipado del archivo combinado `cohort.g.vcf.gz` mediante **GATK GenotypeGVCFs**, generando el archivo `output.vcf.gz`, que contiene las variantes genotipadas:

```
nohup /datos/home/johanlargo/aplicaciones/anaconda3/envs/gwas/bin/gatk --java-options "-Xmx40g -Dtica.numberOfThreads=40" GenotypeGVCFs \
    -R /datos/home/johanlargo/proyectos/20240509-dcl/gatk_resources/reference_genome/Homo_sapiens_assembly38.fasta \
    -V /datos/home/johanlargo/proyectos/20240509-dcl/2_vcf_files/1_only_vcf/cohort.g.vcf.gz \
    -O /datos/home/johanlargo/proyectos/20240509-dcl/2_vcf_files/3_combine_all_vcf/output.vcf.gz &
```

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



```
nohup /datos/home/johanlargo/aplicaciones/anaconda3/envs/gwas/bin/gatk --java-options "-Xmx40g -Dtica.numberOfThreads=40" VariantRecalibrator -V /datos/home/johanlargo/proyectos/20240509-dcl/2_vcf_files/3_combine_all_vcf/output.vcf.gz --trust-all-polymorphic -mode SNP --max-gaussians 6 --resource hapmap,known=false,training=true,truth=true,prior=15:/datos/home/johanlargo/proyectos/20240509-dcl/gatk_resources/hapmap_3.3.hg38.vcf.gz --resource omni,known=false,training=true,truth=true,prior=12:/datos/home/johanlargo/proyectos/20240509-dcl/gatk_resources/1000G_omni2.5.hg38.vcf.gz --resource 1000G,known=false,training=true,truth=false,prior=10:/datos/home/johanlargo/proyectos/20240509-dcl/gatk_resources/1000G_phase1.snps.high_confidence.hg38.vcf.gz --resource dbsnp,known=true,training=false,truth=false,prior=7:/datos/home/johanlargo/proyectos/20240509-dcl/gatk_resources/Homo_sapiens_assembly38.dbsnp138.vcf -an QD -an MQRankSum -an ReadPosRankSum -an FS -an MQ -an SOR -an DP -O /datos/home/johanlargo/proyectos/20240509-dcl/2_vcf_files/3_combine_all_vcf/cohort_snps.recal --tranches-file /datos/home/johanlargo/proyectos/20240509-dcl/2_vcf_files/3_combine_all_vcf/cohort_snps.tranches &
```

2. **ApplyVQSR**: Filtró variantes según el modelo, obteniendo como salida el archivo filtrado `cohort_snps_filtered.vcf.gz`.

```
nohup /datos/home/johanlargo/aplicaciones/anaconda3/envs/gwas/bin/gatk --java-options "-Xmx40g -Dtica.numberOfThreads=40" ApplyVQSR \
    -R /datos/home/johanlargo/proyectos/20240509-dcl/gatk_resources/reference_genome/Homo_sapiens_assembly38.fasta \
    -V /datos/home/johanlargo/proyectos/20240509-dcl/2_vcf_files/3_combine_all_vcf/output.vcf.gz \
    -O /datos/home/johanlargo/proyectos/20240509-dcl/2_vcf_files/3_combine_all_vcf/cohort_snps_filtered.vcf.gz \
    --truth-sensitivity-filter-level 99.0 \
    --tranches-file /datos/home/johanlargo/proyectos/20240509-dcl/2_vcf_files/3_combine_all_vcf/cohort_snps.tranches \
    --recal-file /datos/home/johanlargo/proyectos/20240509-dcl/2_vcf_files/3_combine_all_vcf/cohort_snps.recal \
    -mode SNP &
```

## 4.4 Filtrado de variantes
El comando ejecuta GATK VariantFiltration para filtrar variantes en un archivo VCF (cohort_snps_filtered.vcf.gz) basado en criterios de calidad específicos. A continuación, desgloso cada opción y explico su propósito en el análisis:
```
nohup /datos/home/johanlargo/aplicaciones/anaconda3/envs/gwas/bin/gatk --java-options "-Xmx40g -Dtica.numberOfThreads=40" VariantFiltration \
    -R /datos/home/johanlargo/proyectos/20240509-dcl/gatk_resources/reference_genome/Homo_sapiens_assembly38.fasta \
    -V /datos/home/johanlargo/proyectos/20240509-dcl/2_vcf_files/3_combine_all_vcf/cohort_snps_filtered.vcf.gz \
    -O /datos/home/johanlargo/proyectos/20240509-dcl/2_vcf_files/3_combine_all_vcf/cohort.vqsr.varfilter.vcf.gz \
    --filter-name "LowDP" --filter-expression "DP < 10" \
    --filter-name "LowMQ" --filter-expression "MQ < 40.0" \
    --filter-name "LowQUAL" --filter-expression "QUAL < 30.0" \
    --filter-name "HighSOR" --filter-expression "SOR > 3.0" \
    --filter-name "HighFS" --filter-expression "FS > 60.0" \
    --filter-name "LowMQRankSum" --filter-expression "MQRankSum < -12.5" \
    --filter-name "LowReadPosRankSum" --filter-expression "ReadPosRankSum < -8.0" &
```
### Criterios de filtrado (`--filter-name` y `--filter-expression`)

Para cada criterio, se define un nombre (`--filter-name`) que será usado para marcar las variantes que no cumplan con la expresión lógica especificada (`--filter-expression`). Estos criterios se basan en métricas clave para evaluar la calidad de las variantes:

- **`--filter-name "LowDP"` y `--filter-expression "DP < 10"`**:
  - **DP (Depth of Coverage):** Representa la profundidad de lectura en la posición de la variante.
  - **Razonamiento:** Una cobertura baja (<10) indica poca confianza en la variante, ya que puede ser un artefacto o ruido.

- **`--filter-name "LowMQ"` y `--filter-expression "MQ < 40.0"`**:
  - **MQ (Mapping Quality):** Mide qué tan bien se alinean las lecturas en la variante.
  - **Razonamiento:** Un valor bajo (<40) sugiere que las lecturas no están bien alineadas y podrían ser erróneas.

- **`--filter-name "LowQUAL"` y `--filter-expression "QUAL < 30.0"`**:
  - **QUAL:** Representa la calidad de la llamada de la variante, calculada estadísticamente.
  - **Razonamiento:** Variantes con una calidad baja (<30) tienen alta probabilidad de ser falsos positivos.

- **`--filter-name "HighSOR"` y `--filter-expression "SOR > 3.0"`**:
  - **SOR (Strand Odds Ratio):** Evalúa sesgos en las cadenas de lectura (positiva y negativa).
  - **Razonamiento:** Un valor alto (>3.0) indica que las variantes aparecen principalmente en una cadena, lo que puede ser un artefacto.

- **`--filter-name "HighFS"` y `--filter-expression "FS > 60.0"`**:
  - **FS (Fisher Strand Test):** Detecta sesgos en la distribución de lecturas en las cadenas.
  - **Razonamiento:** Un valor alto (>60) señala que las variantes no están distribuidas uniformemente, lo cual podría ser un artefacto técnico.

- **`--filter-name "LowMQRankSum"` y `--filter-expression "MQRankSum < -12.5"`**:
  - **MQRankSum:** Compara la calidad de mapeo de lecturas de referencia y variantes.
  - **Razonamiento:** Un valor bajo (<-12.5) indica que las variantes podrían estar sesgadas en calidad de mapeo, lo que afecta la confianza en su validez.

- **`--filter-name "LowReadPosRankSum"` y `--filter-expression "ReadPosRankSum < -8.0"`**:
  - **ReadPosRankSum:** Evalúa si las variantes están posicionadas de manera uniforme dentro de las lecturas.
  - **Razonamiento:** Un valor bajo (<-8.0) sugiere que las variantes tienden a aparecer en posiciones específicas dentro de las lecturas, lo que puede indicar artefactos.


Las variantes que pasaron los filtros se extrajeron con **bcftools** y se guardaron en el archivo `cohort_final_filtered.vqsr.varfilter.pass.vcf`.
```
bcftools view -f 'PASS,.' -O vcf -o cohort_final_filtered.vqsr.varfilter.pass.vcf cohort.vqsr.varfilter.vcf.gz
```

Este archivo fue comprimido con **bgzip** 
```
bgzip cohort_final_filtered.vqsr.varfilter.pass.vcf
```
y se generó un índice con **bcftools index**
```
bcftools index cohort_final_filtered.vqsr.varfilter.pass.vcf.gz
```

Obteniendo el archivo final comprimido e indexado `cohort_final_filtered.vqsr.varfilter.pass.vcf.gz`, listo para su uso en análisis posteriores.

### Resumen del archivo generado
con el comando se realizó una visualización inicial del numero total de variantes encontradas:
```
bcftools stats  cohort_final_filtered.vqsr.varfilter.pass.vcf
```
### Resumen de estadísticas del archivo VCF (`cohort_final_filtered.vqsr.varfilter.pass.vcf`)

#### Muestras y registros:
- **Número de muestras**: 20
- **Número total de registros**: 12,834,257
- **Número de sitios sin variantes (no-ALTs)**: 0

#### Tipos de variantes:
- **SNPs**: 10,590,680
- **Indels**: 2,313,544
- **Otros**: 43,868 (variantes complejas o simbólicas)
- **Sitios multialélicos**: 720,689
- **Sitios multialélicos de SNPs**: 23,443

#### Transiciones/Transversiones (Ts/Tv):
- **Número de transiciones (Ts)**: 7,175,615
- **Número de transversiones (Tv)**: 3,435,465
- **Ratio Ts/Tv**: 2.09

#### Singletons (variantes únicas):
- **Número de SNPs singleton**: 3,510,011
- **Transiciones**: 2,384,943
- **Transversiones**: 1,125,068
- **Indels**: 708,127


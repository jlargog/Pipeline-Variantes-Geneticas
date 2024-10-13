# Preparación de Archivos para Análisis Genómicos

En esta primera parte, debemos **alisar los archivos** que nos servirán para realizar todos nuestros análisis en este trabajo. Como se mencionó en la nota de este repositorio, se realizó la descarga de los recursos necesarios.

## Script de Descarga

Para facilitar la descarga, se diseñó un script llamado `download_resources.sh`, que utiliza un bucle `for` para descargar múltiples archivos de datos genómicos desde una URL específica utilizando el comando `wget`. A continuación, se resumen las acciones realizadas por el script:

### Resumen de Acciones

1. Se define una lista de archivos **VCF (Variant Call Format)** y sus índices, que son cruciales para la **anotación** y **análisis de variantes genéticas**.
2. Estos archivos están relacionados con datos de **genomas humanos** y **variantes genéticas**, incluyendo **SNPs (polimorfismos de un solo nucleótido)** y **indels (inserciones y eliminaciones)**.
3. Para cada archivo en la lista, se ejecuta el comando `wget` para descargarlo desde el servidor de almacenamiento de datos genómicos del **Broad Institute** en la ruta especificada.

## Archivos Incluidos en la Descarga

Los siguientes archivos fueron incluidos en la descarga:

- **1000G_omni2.5.hg38.vcf.gz** y su índice.
- **1000G_phase1.snps.high_confidence.hg38.vcf.gz** y su índice.
- **Axiom_Exome_Plus.genotypes.all_populations.poly.hg38.vcf.gz** y su índice.
- **Homo_sapiens_assembly38.dbsnp138.vcf** y su índice.
- **Homo_sapiens_assembly38.known_indels.vcf.gz** y su índice.
- **Mills_and_1000G_gold_standard.indels.hg38.vcf.gz** y su índice.
- **hapmap_3.3.hg38.vcf.gz** y su índice.


# Preprocesamiento de datos genómicos y filtrado de calidad para GWAS  

Este repositorio contiene los pasos para la indexación, anotación y filtrado de variantes antes del análisis de asociación genómica (GWAS). Se parte de un conjunto de variantes en formato VCF y se convierte a formato PLINK aplicando filtros de calidad.

## Pasos del procesamiento  

### 1. **Indexación de archivos VCF**  
Para mejorar la eficiencia en el acceso a los archivos, se realiza la indexación de los archivos de variantes:  

```bash
bcftools index Homo_sapiens_assembly38.dbsnp138.vcf.gz
bcftools index 45_DCL_all_chromosomes.snps.pass.vcf.gz```


### 2. **Anotación de variantes con dbSNP**
Se agrega la información del identificador de variantes (ID) desde la base de datos dbSNP al archivo de variantes de interés:



bash
bcftools annotate -a ../../2_vcf_files/3_combine_all_vcf/Homo_sapiens_assembly38.dbsnp138.vcf.gz -c ID 45_DCL_all_chromosomes.snps.pass.vcf.gz -O z -o updated_45_snps.vcf.gz
3. Conversión a formato PLINK
Se convierte el archivo VCF anotado a formato PLINK (archivos .bed, .bim, .fam):

bash
Copy
Edit
plink --vcf updated_45_snps.vcf.gz --make-bed --out update_45 --allow-extra-chr
4. Edición del archivo FAM
El archivo update_45.fam puede ser editado manualmente con vim o cualquier otro editor de texto en caso de que sea necesario ajustar las etiquetas de fenotipos o IDs.

bash
Copy
Edit
vim update_45.fam
5. Filtrado de calidad genotípica
Se eliminan variantes y muestras con baja calidad mediante los siguientes filtros:

Filtrado por tasa de genotipado:
Se eliminan variantes con más del 5% de datos faltantes y muestras con más del 10% de datos faltantes.

bash
Copy
Edit
plink --bfile update_45 --geno 0.05 --mind 0.1 --make-bed --out filtered_data_45 --allow-extra-chr --allow-no-sex
Filtrado por frecuencia alélica mínima (MAF)
Se eliminan variantes con frecuencia alélica menor al 5%.

bash
Copy
Edit
plink --bfile filtered_data_45 --maf 0.05 --make-bed --out filtered_data_maf_45 --allow-extra-chr --allow-no-sex
6. Resultados y análisis GWAS
Tras la aplicación de estos filtros, se obtiene un conjunto de variantes de alta calidad en formato PLINK listo para el análisis de asociación genética (GWAS). Se parte de un número inicial de variantes y se reducen a una cantidad determinada tras los filtros de calidad.

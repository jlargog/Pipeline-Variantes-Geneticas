### Anotación de IDs de variantes (RS) en el archivo VCF

El archivo VCF generado inicialmente no contenía IDs de variantes (RS). Para agregar esta información, se utilizó la base de datos **dbSNP** (versión `dbsnp138`) como referencia. La herramienta **bcftools annotate** permitió incorporar los IDs correspondientes a las variantes presentes en el archivo `cohort_final_filtered.vqsr.varfilter.pass.vcf.gz`.

El comando utilizado fue el siguiente:

```
bcftools annotate -a Homo_sapiens_assembly38.dbsnp138.vcf.gz -c ID cohort_final_filtered.vqsr.varfilter.pass.vcf.gz -O z -o updated_cohort.vcf.gz
```
### Detalles del proceso:

#### Base de datos de referencia (`-a`):
- Se utilizó `Homo_sapiens_assembly38.dbsnp138.vcf.gz`, que contiene información de variantes conocida, incluyendo IDs (RS).
- **Nota importante**: Este archivo debe estar comprimido en formato `.gz` y debe tener un índice generado con `bcftools index`.

#### Columna de anotación (`-c ID`):
- La opción `-c ID` indica que solo se extraerán los IDs (RS) de la base de datos de dbSNP y se anotarán en el archivo VCF de entrada.

#### Archivo de entrada (`cohort_final_filtered.vqsr.varfilter.pass.vcf.gz`):
- Este archivo contiene las variantes filtradas que necesitan ser anotadas con los IDs de dbSNP.

#### Archivo de salida (`updated_cohort.vcf.gz`):
- El archivo resultante, `updated_cohort.vcf.gz`, es un VCF anotado que incluye los IDs de las variantes presentes en la base de datos dbSNP.

### Consideraciones importantes:
El archivo de referencia (`Homo_sapiens_assembly38.dbsnp138.vcf`) debe estar comprimido en `.gz` y tener su índice (`.tbi`) previamente generado. Esto se logra con los comandos:

```
bgzip Homo_sapiens_assembly38.dbsnp138.vcf
bcftools index Homo_sapiens_assembly38.dbsnp138.vcf.gz
```

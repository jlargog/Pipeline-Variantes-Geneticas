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
## Convertir el archivo VCF a formato PLINK
El primer paso es convertir el archivo VCF a un formato compatible con PLINK, como BED/BIM/FAM, utilizando el siguiente comando
```
plink --vcf ../3_combine_all_vcf/updated_cohort.vcf.gz --make-bed --out cohort_filtered_update --allow-extra-chr
```
### Nota importante:
El error que podrías encontrar se debe a que PLINK detecta un código de cromosoma no estándar en tu archivo VCF, como `chr1_KI270706v1_random`. Esto ocurre porque algunos identificadores de cromosomas presentes en el archivo VCF no son reconocidos por PLINK. Para resolverlo, se utiliza la opción --allow-extra-chr, que permite procesar cromosomas adicionales o no estándar.

## Crear un archivo de fenotipos
El siguiente paso es generar un archivo de fenotipos (.fam) que indique a PLINK cuáles muestras son casos y cuáles son controles.

Si ya has generado el archivo .fam usando el comando anterior, puedes editarlo directamente.
Alternativamente, puedes crear un archivo nuevo con el siguiente formato:
Formato del archivo .fam:
El archivo debe contener una línea por muestra, con las siguientes columnas separadas por espacios:

FID: ID de la familia.
IID: ID individual.
PID: ID del padre (0 si no se conoce).
MID: ID de la madre (0 si no se conoce).
Sexo: 1 = masculino, 2 = femenino, 0 = desconocido.
Fenotipo: 1 = control, 2 = caso, -9 = desconocido.
Ejemplo de archivo .fam:

```
DCL_003 DCL_003 0 0 2 2
DCL_005 DCL_005 0 0 2 1
DCL_008 DCL_008 0 0 1 1
DCL_009 DCL_009 0 0 2 2
DCL_012 DCL_012 0 0 2 2
DCL_014 DCL_014 0 0 1 1
DCL_015 DCL_015 0 0 2 1
DCL_016 DCL_016 0 0 2 2
DCL_020 DCL_020 0 0 2 1
DCL_021 DCL_021 0 0 1 2
DCL_023 DCL_023 0 0 2 2
DCL_024 DCL_024 0 0 2 1
DCL_026 DCL_026 0 0 1 2
DCL_027 DCL_027 0 0 1 1
DCL_042 DCL_042 0 0 2 1
DCL_044 DCL_044 0 0 2 2
DCL_047 DCL_047 0 0 2 1
DCL_048 DCL_048 0 0 2 1
DCL_055 DCL_055 0 0 2 2
DCL_058 DCL_058 0 0 2 2
```





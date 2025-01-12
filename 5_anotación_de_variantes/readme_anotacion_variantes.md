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

### Filtro pre GWAS

Se decide aplicar filtros a cohort_filtered_update

## Eliminar SNPs y muestras con alto nivel de falta de datos:
  plink --bfile cohort_filtered_update --geno 0.05 --mind 0.1 --make-bed --out filtered_data --allow-extra-chr

Criterios de filtrado
--geno 0.05:

Elimina variantes con más del 5% de datos faltantes (genotipos no determinados).
Resultado: 849,584 variantes eliminadas.
--mind 0.1:

Elimina muestras (individuos) con más del 10% de datos genotípicos faltantes.
Resultado: 0 personas eliminadas (todas las muestras tienen suficientes genotipos válidos).
--allow-extra-chr:

Permite incluir cromosomas no estándar en el análisis.
--make-bed:

Genera un conjunto de datos filtrados en formato binario PLINK (.bed/.bim/.fam).

  

## Filtrar por frecuencia alélica menor (MAF):
  plink --bfile filtered_data --maf 0.05 --make-bed --out filtered_data_maf --allow-extra-chr

Criterios de filtrado
--maf 0.05:

Se eliminan variantes con una frecuencia del alelo menor inferior al 5%.
Variantes eliminadas: 4,145,621.
Variantes restantes: 7,839,052.
--allow-extra-chr:

Permite incluir cromosomas no estándar en el análisis.
--make-bed:

Genera un conjunto de datos filtrados en formato binario PLINK (.bed/.bim/.fam).


### Opción logistic
EN nuestro caso como tenemos un diseño experimental de tipo binario donde tenemos casos y controles se optó por realizar una regresión logistica con el fin de integrar diferentes variables. 

--logistic:
Realiza un análisis de regresión logística.
Permite ajustar por covariables (por ejemplo, edad, género, factores ambientales, etc.).
Genera estadísticas adicionales, como betas, errores estándar y valores p, que son útiles para interpretar la fuerza y dirección de las asociaciones.

Para esta ocasión se optaron por tre variables: Edad Escolaridad Consumo_Alcohol Consumo_Cigarrillo. Aunque se tienen conocimiento que DCL posee variabilidad o subtipos, el tamaño de la muestra no permite realizar un analisisi significativo debido a que se evaluaria entre 10 casos. SIn embargo, se tienen estas covariables que se utilizaron para ver la relación de los SNPs utilizados. 

Para esto se debe utilizar un archicho de txt que contenta la información de las covariables, para este caso es covariates.txt y este debe tener el siguiente formato
El archivo covariates.txt es un documento de texto estructurado que contiene información de las covariables asociadas a cada individuo en un estudio genómico. Este archivo es esencial para realizar análisis de asociación que incluyan ajustes por covariables, como la edad, nivel de escolaridad o hábitos relacionados al consumo de sustancias. A continuación, se detalla el significado de cada columna y el formato general del archivo.

FID (Family ID):

Identificador único de la familia del individuo.
En este caso, cada individuo tiene un valor único, lo que implica que no hay relaciones familiares incluidas.
IID (Individual ID):

Identificador único del individuo.
En este estudio, FID e IID son iguales, lo que simplifica el análisis.
Edad:

Edad del individuo en años.

Escolaridad
0=Ninguna
1=Bachiller
2=Técnica profesional
3=Universitaria
4=Postgrado

Consumo de Alcohol (clave)
0=No consumo
1=Socialmente
2=Frecuentemente
3=Alcoholismo activo
4=Alcohlismo inactivo

Consumo de Cigarrillo (clave)
0=No consumo
1=Socialmente
2=Frecuentemente
3=Tabaquismo activo
4=Tabaquismo inactivo


FID IID Edad Escolaridad Consumo_Alcohol Consumo_Cigarrillo
DCL_003 DCL_003 64 1 0 0
DCL_005 DCL_005 60 3 1 0
DCL_008 DCL_008 59 3 4 3
DCL_009 DCL_009 58 2 2 2
DCL_012 DCL_012 52 3 0 0
DCL_014 DCL_014 45 3 1 0
DCL_015 DCL_015 49 3 1 0
DCL_016 DCL_016 61 1 0 0
DCL_020 DCL_020 43 4 0 0
DCL_021 DCL_021 65 3 0 0
DCL_023 DCL_023 68 2 0 4
DCL_024 DCL_024 59 4 1 0
DCL_026 DCL_026 48 3 1 0
DCL_027 DCL_027 56 1 2 2
DCL_042 DCL_042 45 2 1 0
DCL_044 DCL_044 53 4 0 0
DCL_047 DCL_047 48 3 1 0
DCL_048 DCL_048 45 2 1 0
DCL_055 DCL_055 59 3 1 0
DCL_058 DCL_058 54 2 0 0

Adicionalemnte, se debe realizar un archivo phenotype.txt que contiene los fenotipos a evaluar en este caso, caso control. El archivo phenotype.txt es un documento de texto estructurado que contiene información sobre el fenotipo de cada individuo en un estudio genómico. En este caso, el archivo identifica si un individuo pertenece al grupo de casos o controles, lo cual es crucial para realizar análisis de asociación genética.


DCL_003 DCL_003 2
DCL_005 DCL_005 1
DCL_008 DCL_008 1
DCL_009 DCL_009 2
DCL_012 DCL_012 2
DCL_014 DCL_014 1
DCL_015 DCL_015 1
DCL_016 DCL_016 2
DCL_020 DCL_020 1
DCL_021 DCL_021 2
DCL_023 DCL_023 2
DCL_024 DCL_024 1
DCL_026 DCL_026 2
DCL_027 DCL_027 1
DCL_042 DCL_042 1
DCL_044 DCL_044 2
DCL_047 DCL_047 1
DCL_048 DCL_048 1
DCL_055 DCL_055 2
DCL_058 DCL_058 2

## Filtrado de cromosomas no estandar 

Filtrado de cromosomas no estándar
Los cromosomas no estándar (por ejemplo, chr1_KI270706v1_random) se identificaron y eliminaron del archivo .bim para restringir el análisis a los cromosomas autosómicos (1-22)

awk '$1 !~ /^[0-9]+$/' filtered_data_maf.bim > non_standard_chromosomes.txt

awk '{if ($1 !~ /^[0-9]+$/) $1 = 0; print}' filtered_data_maf.bim > filtered_data_maf_cleaned.bim

plink --bed filtered_data_maf.bed --bim filtered_data_maf_cleaned.bim --fam filtered_data_maf.fam --make-bed --out autosomal_data_cleaned

plink --bfile autosomal_data_cleaned --logistic --pheno phenotype.txt --covar covariates.txt --covar-name Edad,Escolaridad,Consumo_Alcohol,Consumo_Cigarrillo --out autosomal_gwas --allow-extra-chr

Eliminar cromosomas no estandar: 

awk '$1 != 0' autosomal_gwas.assoc.logistic > autosomal_gwas_cleaned.assoc.logistic

Verificar los cromosmas presentes:

awk '{print $1}' autosomal_gwas_cleaned.assoc.logistic | sort | uniq

Ver el archivo final 

less autosomal_gwas_cleaned.assoc.logistic




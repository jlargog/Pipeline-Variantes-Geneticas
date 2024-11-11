**Nota:** En nuestro caso específico, la secuenciación se realizó utilizando la plataforma MGI. Es importante tener en cuenta que el encabezado de los archivos FASTQ generados por esta plataforma presenta algunas diferencias en comparación con otros formatos estándar.

Este capítulo se dividirá en cuatro secciones, considerando nuestras necesidades específicas.

## Sección 3.1: Asignación del Read Group

Los Read Groups son fundamentales para la identificación y marcaje de duplicados en el proceso de análisis de datos genómicos. Por lo tanto, se recomienda asignar los Read Groups después de realizar el alineamiento.

Para mayor información dirijase a: [Read groups GATK](https://gatk.broadinstitute.org/hc/en-us/articles/360035890671-Read-groups)

### Nota:

La tecnología MGI utiliza un encabezado un poco diferente al que se conoce comúnmente con Illumina:

`@<Flowcell-id><LaneNo><Column><Row><FieldofView></readNumber>`

Esta respuesta fue dada por el usuario [GenoMax](https://www.seqanswers.com/forum/sequencing-technologies-companies/mgiseq-fka-complete-genomics/326115-g400-fastq-header-description).

Por ejemplo, para nuestro archivo `DCL006_E200021112_L01_1_436080_1.fastq`, uno de sus encabezados es: `@E200021112L1C001R00100000007/1`.

Se debe recordar que en nuestro caso se realizó una secuenciación de extremos emparejados (Paired-end) y por lo tanto, los encabezados del otro archivo terminan en /2.

Con respecto a la información que se requiere para la asignación de grupos de lectura, y como esta no podría ser análoga al formato tradicional, se establecen los parámetros que se utilizan a continuación.


### Automatización del Proceso
Se ha desarrollado un script en Python, denominado [`read_group.py`](read_group.py), con el objetivo de automatizar la adición de Read Groups a los archivos `BAM`. Este script simplifica el proceso y asegura que todos los archivos estén correctamente etiquetados, facilitando así un análisis más eficiente y preciso. Esta versión proporciona una estructura más técnica y clara, destacando la importancia de los Read Groups y la automatización del proceso.

Acontinuación se relacionan algunos parametrso del script: 

`bam_directory`: Ruta al directorio que contiene los archivos BAM originales.

`gatk_path`: Ruta al ejecutable de GATK.

`output_directory`: Ruta al directorio donde se guardarán los archivos BAM procesados con Read Groups.

`java_options`: Opciones para la ejecución de Java, en este caso, se establece un límite de memoria máxima de 50 GB.

**Opciones de Read Group:**

`--RGID`: Define el identificador único del Read Group, que se extrae del nombre del archivo BAM.

`--RGLB`: Especifica la biblioteca de origen para las lecturas (en este caso, se ha utilizado un nombre genérico 'mgi_library'). Este campo puede ser útil para identificar la biblioteca utilizada durante la secuenciación.

`--RGPL`: Indica la plataforma utilizada para la secuenciación, en este caso, 'MGI'.

`--RGPU`: Proporciona un identificador único para el flujo de datos o unidad de producción (puede ser el mismo que RGID).

`--RGSM`: Especifica el identificador de la muestra (sample ID) que se extrae del nombre del archivo BAM.

## Sección 3.2: Ordenamiento del archivo BAM

El ordenamiento (o "sort") en los archivos BAM organiza las lecturas alineadas en función de las posiciones genómicas. Esto significa que todas las lecturas que se mapearon en una región específica del genoma estarán juntas en el archivo, ordenadas según su posición de inicio.

### Automatización del Proceso

Para automatizar el proceso de ordenamiento se diseño el script [`sort.py`](sort.py). El script recorre todos los archivos BAM en el directorio de entrada cuyo nombre empieza con "DCL_", los ordena según la coordenada genómica, y genera un archivo BAM ordenado para cada uno en el directorio de salida. Además, cada archivo generado se acompaña de un índice (.bai), necesario para realizar análisis eficientes en otros programas.

## Sección 3.3: Marcado de duplicados del archivo BAM

El marcado de duplicados ayuda a identificar y etiquetar lecturas duplicadas que surgen comúnmente durante el proceso de secuenciación de alto rendimiento. Estas lecturas duplicadas pueden sesgar el análisis de variantes, por lo que es importante identificarlas antes de los análisis posteriores.

### Automatización del Proceso

Se diseñó el script [`mark_duplicates.py`](mark_duplicates.py). Este script recorre todos los archivos BAM ordenados en el directorio de entrada y, para cada archivo, utiliza la herramienta `MarkDuplicates` de Picard para generar un archivo BAM con los duplicados marcados. Además, genera un archivo de métricas que proporciona información detallada sobre la cantidad de duplicados detectados en cada muestra. Este proceso está optimizado para manejar archivos de gran tamaño, especificando parámetros como la memoria máxima y un directorio temporal para mejorar el rendimiento.

El script genera archivos BAM con duplicados marcados y archivos `.txt` que contienen diversas métricas para cada muestra. Los archivos generados incluyen:

- 4.9K marked_dup_metrics_DCL_003_E200015275_L01_41_424524.txt
- 7.7K marked_dup_metrics_DCL_005_E200015275_L01_42_424525.txt
- 6.4K marked_dup_metrics_DCL_008_E200015275_L01_43_424527.txt
- 7.6K marked_dup_metrics_DCL_009_E200015275_L01_44_424528.txt
- 4.3K marked_dup_metrics_DCL_012_E200015275_L01_45_424530.txt
- 7.5K marked_dup_metrics_DCL_014_E200015275_L01_46_424531.txt
- 8.3K marked_dup_metrics_DCL_015_E200015275_L01_47_424532.txt
- 5.8K marked_dup_metrics_DCL_016_E200015275_L01_48_424533.txt
- 5.9K marked_dup_metrics_DCL_020_E200015275_L01_57_424535.txt
- 6.5K marked_dup_metrics_DCL_021_E200015275_L01_58_424536.txt
- 4.6K marked_dup_metrics_DCL_023_E200015233_L01_65_424537.txt
- 7.7K marked_dup_metrics_DCL_024_E200015233_L01_66_424538.txt
- 5.3K marked_dup_metrics_DCL_026_E200015233_L01_67_424540.txt
- 6.7K marked_dup_metrics_DCL_027_E200015233_L01_68_424541.txt
- 5.0K marked_dup_metrics_DCL_042_E200015233_L01_69_424548.txt
- 5.2K marked_dup_metrics_DCL_044_E200015233_L01_70_424549.txt
- 5.5K marked_dup_metrics_DCL_047_E200015233_L01_71_424551.txt
- 5.7K marked_dup_metrics_DCL_048_E200015233_L01_72_424552.txt
- 4.9K marked_dup_metrics_DCL_055_E200015233_L01_73_424554.txt
- 7.6K marked_dup_metrics_DCL_058_E200015233_L01_74_424555.txt


Para combinar y analizar estas métricas, se creó el script en Python [`evaluated_duplicate.py`](evaluated_duplicate.py), que consolida los diferentes archivos `.txt` en un archivo `.csv` llamado `consolidated_duplication_metrics.csv`, facilitando el análisis de calidad de las muestras. Este archivo permite realizar análisis como:

- **Promedio y Desviación Estándar** del `PERCENT_DUPLICATION` para evaluar la duplicación media entre todas las muestras.
- **Gráficos de Barras o Boxplots** para comparar las métricas de duplicación y el tamaño de la biblioteca entre muestras.
- **Análisis de Correlación** para ver si existe alguna relación entre el tamaño de la biblioteca y el porcentaje de duplicación.


## Sección 3.4: Recalibración del archivo BAM

Como parte del posprocesamiento del archivo BAM, se realizó una recalibración de bases. Este proceso consta de varios pasos, comenzando con el **Paso 1 - Construir el Modelo**.

#### Paso 1: Construcción del Modelo
En este paso, se utilizó el script [`recalibrate_part1.py`](recalibrate_part1.py) en Python para ejecutar el comando `BaseRecalibrator` de GATK, el cual genera un archivo de recalibración para cada muestra en el directorio de salida. Este archivo de recalibración contiene las estadísticas necesarias para ajustar las calidades de base.

Este script realiza los siguientes pasos para cada archivo BAM en el directorio de entrada:

1. Extrae el nombre de la muestra del archivo BAM y genera un archivo de salida de recalibración (`.table`) en el directorio de salida.
2. Ejecuta el comando `BaseRecalibrator` de GATK, utilizando:
   - **20 GB de memoria** y **40 hilos** para optimizar el rendimiento.
   - Un archivo de **referencia genómica** y **sitios conocidos** de variantes como entradas necesarias.
3. Captura y escribe la salida y los errores en un archivo `nohup.out` para registro y depuración.
4. Muestra un mensaje de progreso al completar cada archivo BAM.







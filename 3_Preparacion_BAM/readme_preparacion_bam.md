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

Se diseño el script [`mark_duplicates.py`](mark_duplicates.py). El script recorre todos los archivos BAM ordenados en el directorio de entrada, y, para cada archivo, utiliza la herramienta `MarkDuplicates` de Picard para generar un archivo BAM con los duplicados marcados. Adicionalmente, genera un archivo de métricas que proporciona información detallada sobre la cantidad de duplicados detectados en cada muestra. Este proceso está optimizado para manejar archivos de gran tamaño, especificando parámetros como la memoria máxima y un directorio temporal para optimizar el rendimiento.


## Sección 3.4: Recalibración del archivo BAM


**Nota:** En nuestro caso específico, la secuenciación se realizó utilizando la plataforma MGI. Es importante tener en cuenta que el encabezado de los archivos FASTQ generados por esta plataforma presenta algunas diferencias en comparación con otros formatos estándar.

Este capítulo se dividirá en cuatro secciones, considerando nuestras necesidades específicas.

## Sección 3.1: Asignación del Read Group

Es necesario agregar un Read Group a cada archivo BAM para garantizar una correcta interpretación de los datos durante el análisis posterior.
Importante: Los Read Groups son fundamentales para la identificación y marcaje de duplicados en el proceso de análisis de datos genómicos. Por lo tanto, se recomienda asignar los Read Groups después de realizar el alineamiento.

Para mayor información dirijase a: [Read groups GATK](https://gatk.broadinstitute.org/hc/en-us/articles/360035890671-Read-groups)

### Automatización del Proceso
Se ha desarrollado un script en Python, denominado ['read_group.py'](read_group.py), con el objetivo de automatizar la adición de Read Groups a los archivos BAM. Este script simplifica el proceso y asegura que todos los archivos estén correctamente etiquetados, facilitando así un análisis más eficiente y preciso. Esta versión proporciona una estructura más técnica y clara, destacando la importancia de los Read Groups y la automatización del proceso.


## Sección 3.2: Ordenamiento del archivo BAM

## Sección 3.3: Marcado de duplicados del archivo BAM

## Sección 3.4: Recalibración del archivo BAM


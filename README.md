# Pipeline Variantes Genéticas
Tools and step-by-step for genome assembly

Hola, se crea este repositorio en español con el fin de documentar una linea de trabajo para el ensamblaje de genomas en Humanos.
Antes de de todo, los comandos se ejecutaran mediante un entorno ANACONDA. Si desea realizar la instalación de ANACONDA vaya al siguiente repositorio 

**NOTA:** Se tuvo en cuenta el taller documentado por Mellbourne Bioinformatics de la Universidad de Mellbourne. Puede consultar el taller y procedimientos en: [Variant calling using GATK4](https://www.melbournebioinformatics.org.au/tutorials/tutorials/variant_calling_gatk1/variant_calling_gatk1/#3-base-quality-recalibration) agradecer al autor Khalid Mahmood
Developed: July 2021
Reviewed: June 2023

## Índice de capítulos
[Capítulo 1: Preparativos iniciales](/1_preparativos_iniciales/descargas.md)

[Capítulo 2: Alineamiento](readme_alineamiento.md)





Se realizan ajustes según las necesidades y se documenta lo siguiente:

## Control de Calidad
Un primer paso para el analisis de datos genómicos, trasncriptómicos, proteómicos entre otros, es realizar un control de calidad a las lecturas que recibimos de nuestra tecnología de secuenciación. Para esto se utilizarán los programas "Gold   standar" para tal fin, entre lso cuales están FastQC, MultiQC y Trimmomatic. 
 
### Visualización Inicial
Se crea un script en python que permita manejar directorios que permita procesar varios archivos fastq a la vez.
Se inicia una primera visualización del estado de las librerias utilizando el script de python fastqc.py
`nohup python3 fastqc.py &`

Se ejecuta MultiQC en la carpeta de resultados de FastQC
`multiqc 1_quality_visual/ -o 1_quality_visual/`

Se establece que para realizar el respectivo control de calidad de las secuencias, se va a implementará el programa Trimmomatic. En los reportes de FastQC se evidencian cadenas PolyA y PolyG, asi que se modifica el archivo de adaptadores para que este tenga las secuencias PolyA que está identificando FastQC y MultiQC.

```plaintext
TruSeq3-PE.fa
>PrefixPE/1
TACACTCTTTCCCTACACGACGCTCTTCCGATCT
>PrefixPE/2
GTGACTGGAGTTCAGACGTGTGCTCTTCCGATCT
>PolyA
AAAAAAAAAAAA
>PolyT
TTTTTTTTTTTT
>PolyG
GGGGGGGGGGGG
```
Se realizó un script con Trimmomatic recortetrim.py

## Preparación del Genoma de Referencia

**NOTA:** Se realizarón varias pruebas hasta en donde se evidenció que el genoma de referencia descargado por la base de datos del NCBI, debía tener un archivo vcf especifico, por problemas de compatibilidad se decidió descargar los recursos sugeridos por el GATK. 

`nohup wget -c https://storage.googleapis.com/genomics-public-data/resources/broad/hg38/v0/Homo_sapiens_assembly38.fasta &`

`nohup wget -c https://storage.googleapis.com/genomics-public-data/resources/broad/hg38/v0/Homo_sapiens_assembly38.dbsnp138.vcf &`

### Indexación del Genoma de Referencia
Para tal fin se utilizó el siguiente comando:
`nohup bwa index Homo_sapiens_assembly38.fasta &`

## Ensamblaje hacia el Genoma de Referencia

### Preparación del Archivo BAM

**NOTA:** Como se realizarón varias pruebas y el espacio en el servidor era limitado, se realizó el ensamblaje con los datos crudos. Tener en cuenta que se recomienda ensamblar con los archivos fastq que arroja el proceso de limpieza con Trimmomatic.
Para mapear las lecturas se utilizó el programa BWA con las siguientes especificaciones.

`nohup bwa mem -t 40 /datos/home/johanlargo/proyectos/20230703-alzheimer/gatk_resources/index_bwa/Homo_sapiens_assembly38.fasta /datos/home/johanlargo/proyectos/20230703-alzheimer/0_rawdata/data/751/751_R1.fastq.gz /datos/home/johanlargo/proyectos/20230703-alzheimer/0_rawdata/data/751/751_R2.fastq.gz -o /datos/home/johanlargo/proyectos/20230703-alzheimer/4_assembly_bwa/751.sam &`

Se convierte de sam a bam con:

`nohup samtools view -@ 40 -bS 751.sam -o 751.bam &`

### Ordenamiento del Archivo BAM 

Se realiza un ordenamiento del archivo bam:

**NOTA:** Se generaron problemas de almacenamiento con la carpeta tmp:
Se establece tempoalmente la carpeta tmp

`nohup java -Djava.io.tmpdir=/datos/home/johanlargo/tmp -Xmx100g -jar /datos/home/johanlargo/aplicaciones/anaconda3/envs/gwas/share/picard-2.27.5-0/picard.jar SortSam I=/datos/home/johanlargo/proyectos/20230703-alzheimer/4_assembly_bwa/751.bam O=/datos/home/johanlargo/proyectos/20230703-alzheimer/4_bam_sorted/751.sorted.bam VALIDATION_STRINGENCY=LENIENT SORT_ORDER=coordinate MAX_RECORDS_IN_RAM=3000000 CREATE_INDEX=True &`

### Marcado de Duplicados

Ahora, se continua con el marcado de duplicados:

`nohup java -Djava.io.tmpdir=/datos/home/johanlargo/tmp -Xmx100g -jar /datos/home/johanlargo/aplicaciones/anaconda3/envs/gwas/share/picard-2.27.5-0/picard.jar MarkDuplicates I=/datos/home/johanlargo/proyectos/20230703-alzheimer/4_bam_sorted/751.sorted.bam O=/datos/home/johanlargo/proyectos/20230703-alzheimer/4_mark_duplicates/751.sort.dup.bam METRICS_FILE=/datos/home/johanlargo/proyectos/20230703-alzheimer/4_mark_duplicates/marked_dup_metrics_751.txt &`

### Recalibración de Bases 

#### Paso 1 Construcción del Modelo
A la hora de realizar la recalibración de bases, paso fundamental según los procedimientos del GATK. Arroja el siguiente error:

error "Number of read groups must be >= 1, but is 0" indica que el archivo de entrada BAM no contiene información sobre grupos de lecturas (read groups).

Se sugiere aplicar el siguiente comando:

`/datos/home/johanlargo/aplicaciones/anaconda3/envs/gwas/bin/gatk --java-options "-Xmx50g" AddOrReplaceReadGroups -I /datos/home/johanlargo/proyectos/20230703-alzheimer/4_mark_duplicates/751.sort.dup.bam -O /datos/home/johanlargo/proyectos/20230703-alzheimer/4_mark_duplicates/751.sort.dup.rg.bam --RGID 1 --RGLB library --RGPL Illumina --RGPU unit --RGSM sample`

`nohup /datos/home/johanlargo/aplicaciones/anaconda3/envs/gwas/bin/gatk --java-options "-Xmx100g -Dtica.numberOfThreads=40" BaseRecalibrator -I /datos/home/johanlargo/proyectos/20230703-alzheimer/4_mark_duplicates/751.sort.dup.rg.bam -R /datos/home/johanlargo/proyectos/20230703-alzheimer/gatk_resources/Homo_sapiens_assembly38.fasta --known-sites /datos/home/johanlargo/proyectos/20230703-alzheimer/gatk_resources/vcf/Homo_sapiens_assembly38.dbsnp138.vcf -O /datos/home/johanlargo/proyectos/20230703-alzheimer/4_base_quality_recalibration/recal_data.table &`

#### Paso 2 Aplicar el Modelo Ajustado a las Puntuaciones de Calidad


![image](https://github.com/jlargog/Pipeline-Variantes-Geneticas/assets/138719333/38aa0896-c99e-4a30-a796-386ebaee0e83)





















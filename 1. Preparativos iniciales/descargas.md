En una primera parte, debemos alistar los archivos que nos van a servir para realizar todos nuestros analisis en este trabajo. Como se mencionó en la Nota de este repositorio, se realizó la descarga de los recursos.

Para facilidad en la descarga, se diseño un script download_resources.sh que utiliza un bucle for para descargar múltiples archivos de datos genómicos desde una URL específica utilizando el comando wget. A continuación se resumen las acciones realizadas por el script:

Resumen:
Se define una lista de archivos VCF (Variant Call Format) y sus índices, que son cruciales para la anotación y análisis de variantes genéticas. Estos archivos están relacionados con datos de genomas humanos y variantes genéticas, incluyendo SNPs (polimorfismos de un solo nucleótido) y indels (inserciones y eliminaciones).
Para cada archivo en la lista, se ejecuta el comando wget para descargarlo desde el servidor de almacenamiento de datos genómicos de Broad Institute en la ruta especificada.

Archivos incluidos en la descarga:
1000G_omni2.5.hg38.vcf.gz y su índice.
1000G_phase1.snps.high_confidence.hg38.vcf.gz y su índice.
Axiom_Exome_Plus.genotypes.all_populations.poly.hg38.vcf.gz y su índice.
Homo_sapiens_assembly38.dbsnp138.vcf y su índice.
Homo_sapiens_assembly38.known_indels.vcf.gz y su índice.
Mills_and_1000G_gold_standard.indels.hg38.vcf.gz y su índice.
hapmap_3.3.hg38.vcf.gz y su índice.

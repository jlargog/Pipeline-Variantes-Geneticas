#!/bin/bash

# Directorio donde se encuentran los archivos VCF
vcf_dir="/datos/home/johanlargo/proyectos/20240509-dcl/2_vcf_files/1_only_vcf"

# Archivo de salida para el resumen
output_summary="vcf_statistics_summary.csv"

# Crear encabezado del archivo resumen
echo "Archivo,Total Variantes,SNPs,Indels,MNPs,Otros" > $output_summary

# Procesar cada archivo VCF
for vcf_file in $vcf_dir/*.vcf.gz; do
    echo "Procesando $vcf_file..."
    
    # Generar estadísticas con bcftools
    stats_file="${vcf_file}.stats"
    bcftools stats $vcf_file > $stats_file
    
    # Extraer estadísticas específicas
    total_variants=$(grep "^SN" $stats_file | grep "number of records:" | awk '{print $NF}')
    snps=$(grep "^SN" $stats_file | grep "number of SNPs:" | awk '{print $NF}')
    indels=$(grep "^SN" $stats_file | grep "number of indels:" | awk '{print $NF}')
    mnps=$(grep "^SN" $stats_file | grep "number of MNPs:" | awk '{print $NF}')
    others=$(grep "^SN" $stats_file | grep "number of others:" | awk '{print $NF}')
    
    # Añadir estadísticas al archivo resumen
    echo "$(basename $vcf_file),$total_variants,$snps,$indels,$mnps,$others" >> $output_summary
done

echo "Estadísticas recopiladas en: $output_summary"


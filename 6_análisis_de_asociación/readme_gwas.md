  
    <h2>Descripción</h2>
    <p>Este repositorio contiene un conjunto de comandos utilizados para procesar datos de variantes genéticas en formato VCF y convertirlos a formato PLINK para realizar un análisis de asociación de genoma completo (GWAS). Se incluyen pasos para indexar, anotar, filtrar y convertir los datos de variantes genéticas.</p>
    
    <h2>Pasos del proceso</h2>
    
    <h3>1. Indexación de archivos VCF</h3>
    <p>Se indexan los archivos VCF para optimizar su acceso mediante BCFtools:</p>
    <pre><code>bcftools index Homo_sapiens_assembly38.dbsnp138.vcf.gz
bcftools index 45_DCL_all_chromosomes.snps.pass.vcf.gz</code></pre>
    
    <h3>2. Anotación de variantes</h3>
    <p>Se utiliza BCFtools para anotar las variantes en el archivo VCF de estudio con información del archivo de referencia <code>dbSNP</code>.</p>
    <pre><code>bcftools annotate -a ../../2_vcf_files/3_combine_all_vcf/Homo_sapiens_assembly38.dbsnp138.vcf.gz -c ID 45_DCL_all_chromosomes.snps.pass.vcf.gz -O z -o updated_45_snps.vcf.gz</code></pre>
    
    <h3>3. Conversión a formato PLINK</h3>
    <p>Se convierte el archivo VCF a formato PLINK (<code>.bed</code>, <code>.bim</code>, <code>.fam</code>) utilizando el siguiente comando:</p>
    <pre><code>plink --vcf updated_45_snps.vcf.gz --make-bed --out update_45 --allow-extra-chr</code></pre>
    
    <h3>4. Edición manual del archivo <code>.fam</code></h3>
    <p>El archivo <code>update_45.fam</code> puede requerir modificaciones manuales en el editor <code>vim</code> para corregir datos de muestras si es necesario.</p>
    <pre><code>vim update_45.fam</code></pre>
    
    <h3>5. Filtrado de calidad de genotipos</h3>
    <p>Se eliminan variantes y muestras con baja calidad, usando filtros de tasa de genotipado (<code>geno 0.05</code>) y tasa de individuos faltantes (<code>mind 0.1</code>).</p>
    <pre><code>plink --bfile update_45 --geno 0.05 --mind 0.1 --make-bed --out filtered_data_45 --allow-extra-chr --allow-no-sex</code></pre>
    
    <h3>6. Filtrado por frecuencia alélica mínima (MAF)</h3>
    <p>Se filtran las variantes con una frecuencia alélica mínima (<code>maf 0.05</code>).</p>
    <pre><code>plink --bfile filtered_data_45 --maf 0.05 --make-bed --out filtered_data_maf_45 --allow-extra-chr --allow-no-sex</code></pre>
    
    <h2>Resultados</h2>
    <ul>
        <li>Se obtiene un conjunto de datos en

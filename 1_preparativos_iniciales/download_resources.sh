for file in "1000G_omni2.5.hg38.vcf.gz" "1000G_omni2.5.hg38.vcf.gz.tbi" "1000G_phase1.snps.high_confidence.hg38.vcf.gz" "1000G_phase1.snps.high_confidence.hg38.vcf.gz.tbi" "Axiom_Exome_Plus.genotypes.all_populations.poly.hg38.vcf.gz" "Axiom_Exome_Plus.genotypes.all_populations.poly.hg38.vcf.gz.tbi" "Homo_sapiens_assembly38.dbsnp138.vcf" "Homo_sapiens_assembly38.dbsnp138.vcf.idx" "Homo_sapiens_assembly38.known_indels.vcf.gz" "Homo_sapiens_assembly38.known_indels.vcf.gz.tbi" "Mills_and_1000G_gold_standard.indels.hg38.vcf.gz" "Mills_and_1000G_gold_standard.indels.hg38.vcf.gz.tbi" "hapmap_3.3.hg38.vcf.gz" "hapmap_3.3.hg38.vcf.gz.tbi"
do
    wget https://storage.googleapis.com/genomics-public-data/resources/broad/hg38/v0/"$file"
done


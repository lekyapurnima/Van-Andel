Questions for Van Andel Institute

1. Variant type (e.g. insertion, deletion, etc.)
- The variant type was calculated based on the length of variant bases. If reference base length equals variant base length it is called as a "snp",
if referernce base length is shorter than variant base length it is called as "insertion", if reference base lenfth is longer than variant base length it is called as "deletion". This is present in the column number 5.

2. Variant effect.
- The variant effect was retreived by querying the exac database using rest api. If the variant doesn't exist for a variation the code returns it as no consequence.
- In some cases there are multiple consequnces for a variant episode. I didn't find time to extract the deleterious effect. But i have return another script in the folder named "variant_impacy.py" which reads in the file variant_effect.txt and categorises various consequences into High, Moderate, Low and Modifier. The information in variant_impact.tsv is extracted from ensembl website. The original idea was to match all the variants for a event from exac database and look into the categories from the above script and report the highest or deleterious effect. For now i have retrevived all the possible consequences for a variant for snps and indels. They are in the column 6 of the output.

3. Read depth at site of variation
- The second column second element describes the read depth at site of variation

4. Number of reads supporting the variant
- The second column second element describes the read depth at site of variation

5. Percentage of reads supporting the variant vs reference reads.
- This was calculated bases on the filtered reads supporting the reference and variation. They were added to get a total number of reads for the reion and percentages were calculated from it for each of the reference and the varation. They are in the column 3,4

6. Allele frequency of the variant
- Allele frequency of the variant is queried from the exac. For snp if if there are multiple consequences there will be only one allele_frequency value which is reported in column 7. For indel there are multiple consequences with multiple allel_frequency which are reported in the same column as a list.
#Import of modules
import requests
import csv
import json
import objectpath


#Function to get variants compatible for rest format.
##the function takes in coding_challenge.vcf from the same directory extract the
#chromosome number, position of variantion, reference base and alternate base along with the
#reads supporting the reference base and variant base
def variants():
    vcf = open("coding_challenge.vcf", "r")
    out = []
    for line in vcf:
        if not line.startswith("#"):
            lis = line.split("\t")
            chromosome,position,REF,ALT = lis[0].split("r")[1],lis[1],lis[3],lis[4]
            ad = lis[9].split(":")[3]
            ##if multiallelic looks for ',' in variant bases columns and splits and write them in 
            ## as multiallelic rows
            if ',' in ALT:
                strVars = ALT.split(',')
                multialleles = len(strVars)
                for i in range(0, multialleles):
                    variant = chromosome + '-' + position + '-' + REF + '-' + strVars[i] + "\t" \
                         + ad.split(",")[0] + ',' + ad.split(",")[i] + "\n"
                    out.append(variant)
            else:
                variant = chromosome + '-' + position + '-' + REF + '-' + ALT + "\t" + ad + "\n"
                out.append(variant)
    return out

##function to calculate the percentage of reads supporting the reference vs
#percentage of reads supporting the variantion. they are counted based on the filtered reads columns.
#Some can be zero because the reads under a quality score gets filtered.
#the function appends percentages to the output from variants function
def percentages():
    percentages_fun = variants()
    percents = []
    for i in percentages_fun:
        i = i.rstrip()
        reads = i.split("\t")[1].split(',')
        reference_support = int(reads[0])
        variant_support = int(reads[1])
        total_reads = reference_support + variant_support
        try:
            variant_percent = (variant_support*100)/total_reads
            reference_percent = 100-variant_percent
        except ZeroDivisionError as ze:
            variant_percent = 0
            reference_percent = 0
        percents.append(i + "\t" + str(reference_percent) + "\t" + str(variant_percent) + "\n")
    return percents


#Function to add snp or insertion or deletion
#this function adds a column to the above data if the variation is snp, insertion or deletion.
#this was calculated base on the variant bases.If reference base length equals variant base length it is called as a snp
#if referernce base length is shorter than variant base length it is called as insertion
#if reference base lenfth is longer than variant base length it is called as deletion
#this id appended to the existing data
def type_variant():
    type_fun = percentages()
    lis = []
    for i in type_fun:
        variant = i.split("\t")[0]
        ref = variant.split("-")[2]
        alt = variant.split("-")[3]
        if len(ref) == len(alt):
            lis.append(i.rstrip() + "\t" + "snp")
        elif len(ref) > len(alt):
            lis.append(i.rstrip() + "\t" + "deletion")
        elif len(ref) < len(alt):
            lis.append(i.rstrip() + "\t" + "insertion")
        else:
            print ("line empty")
    return lis

##Function to get the effect of variant from rest exac database.
##one of the major function which queries the exac database to get the effect of variation along with allele_frequency
#the function takes in the above data which is already in the querying format for rest api to exac database.
#split and queried. A module named requests is used to query information

##the function also creates a ouput file named variant_effect.txt which is a tab separated file with following columns
# 1. rest_format of the varaint of vcf file
# 2. reference read depth, variant read depth
# 3. percentage of reference reads
# 4. percentage of variation reads
# 5. variant type
# 6. variant consequence
# 7. allele_frequency
def variant_effect():
    out = open("variant_effect.txt", "w")
    header = ("#rest_format" + "\t" + "refernce_depth,variant_depth" +  "\t" + "percent_reads_for_reference" + "\t" + "percent_reads_for_variant" \
    + "\t" + "variant_type" + "\t" + "variant_consequence" + "\t" + "allele_frequency" + '\n')
    out.write(header)
    variant_effect_fun = type_variant()
    dict = {}


    for variant in variant_effect_fun:

        ## if the variant is a snp they can be queried used rest/variant api
        if variant.split("\t")[4] == "snp":
            variant_format = variant.split("\t")[0]
            rest_variant = requests.get("http://exac.hms.harvard.edu/rest/variant/%s" % variant_format)
            if rest_variant.status_code == 200:
                res = (rest_variant.json())
                dict[variant] = res
        #     #print (dict[variant]['variant']["allele_freq"])
                if dict[variant]['consequence'] is None:
                    out.write(variant + "\t" + "no consequence" + "\t" + "no allele frequency" + "\n")
                else:
                    out.write(variant + "\t" + str(dict[variant]['consequence'].keys()) + "\t" + str(dict[variant]['variant']['allele_freq']) + "\n")

        ## if the variant is a inserion/deleted they can be queried used rest/region api
        elif variant.split("\t")[4] == "insertion" or variant.split("\t")[4] == "deletion":
            variant_format = variant.split("\t")[0]
            len_variant = len(variant_format.split("-")[2])
            change_format = int(variant_format.split("-")[1]) + (len_variant - 1)
            region = variant_format.split("-")[0]+ "-" + variant_format.split("-")[1] + "-" + str(change_format)
            rest_variant = requests.get("http://exac.hms.harvard.edu/rest/region/%s" % region.rstrip())
            # # change in variant format for region
            res = (rest_variant.json())
            dict[variant] = res
        
            if len(dict[variant]["variants_in_region"]) == 0:
                out.write(variant + "\t" + "no consequence" + "\t" + "no allele frequency" + "\n")
            else:
                region = dict[variant]["variants_in_region"]
                jsonnn_tree = objectpath.Tree(dict[variant])
                major_consequence = tuple(jsonnn_tree.execute('$..major_consequence'))
                allele_frequency = tuple(jsonnn_tree.execute('$..allele_freq'))
                out.write(variant + "\t" + str(major_consequence) +  "\t" + str(allele_frequency) + "/n")

        else:
            print("Something went wrong")
            print(rest_variant.status_code)
            # x = rest_variant.json()
            # print(x)


##complete script will be called with single fucntion
variant_effect()
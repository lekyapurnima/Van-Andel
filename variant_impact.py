
def variant(file):
    variant_impact = open(file, 'r')

    dict = {}

    high = []
    moderate = []
    low = []
    modifier = []
    for line in variant_impact:
        variant = line.split("\t")
        if variant[4].rstrip() == "HIGH":
            high.append(variant[0])
        elif variant[4].rstrip() == "MODERATE":
            moderate.append(variant[0])
        elif variant[4].rstrip() == "LOW":
            low.append(variant[0])
        elif variant[4].rstrip() == "MODIFIER":
            modifier.append(variant[0])
        else:
            print ("out of bounds")

    dict["high"],dict["moderate"],dict["low"],dict["modifier"] = high,moderate,low,modifier
    return dict

def main():
    x  = variant("variant_impact.tsv")
    print (x)

if __name__ == "__main__":
    main()
import csv
import json

"""
This file is to clean the raw nutrient data. 
"""

ELEMENT_TUPLE = ('nf_protein','nf_dietary_fiber','nf_vitamin_a_dv','nf_vitamin_c_dv','nf_calcium_dv', 'nf_iron_dv',
     'nf_sodium','nf_calories','nf_serving_weight_grams',"key_ingredient")

def get_nutrient_clean(fclean, fraw):
    """Extract clean data and save to file.
    Arguments:
        fclean {string} -- file to be saved
        fraw {string} -- file to be clean
    """
    nutrient_clean = open(fclean, 'w')
    csvwriter = csv.writer(nutrient_clean)
    i = 0
    with open(fraw, "r") as f:
        for line in f:
            i += 1
            try:
                detail = json.loads(line)
                result = {k:v for k, v in detail.items() if k in ELEMENT_TUPLE}
                if i == 1:
                    header = result.keys()
                    csvwriter.writerow(header)
                csvwriter.writerow(result.values())
            except IndexError:
                pass
    nutrient_clean.close()



def main():
    get_nutrient_clean('nutrient_clean.csv', 'nutrient.txt')

if __name__== "__main__":
  main()
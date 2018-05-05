from nutritionix import Nutritionix
import pickle  
import json  
"""
This file is to scrape nutritional information from nutritionix API. 
"""

START = 0
# please add your app_id and api_key
APP_ID = ""
API_KEY = ""

def load_pickle(fname):
    """load the pickle file to get all the food.
    Arguments:
        fname {string} -- file to be loaded
    """
    with open(fname, 'rb') as f:
        total_food = pickle.load(f) 
    return total_food

def get_nutrient(food):
    """Hepler function to get raw data for a food from API.
    Arguments:
        food {string} -- food to be found
    Returns:
        detail {dictionary} -- raw data is store in the dictionary
    """
    nix = Nutritionix(app_id=APP_ID, api_key="")
    a = nix.search(food, results="0:1").json()
    detail = {}
    if 'hits' in a:
        hits = a['hits']
        try:
            item_id = hits[0]['_id']
            detail = nix.item(id=item_id).json()
        except IndexError:
            pass
    detail["key_ingredient"] = food
    print(detail["key_ingredient"])
    return detail

def get_nutrient_raw(total_food):
    """Get get raw data for all the food from API.
    Arguments:
        total_food {list of string} -- all the food to be found
    """
    fname = "nutrient_"+str(START)+".txt"
    with open(fname, "w") as f:
        for food in total_food:
            data = get_nutrient(food)
            f.write(json.dumps(data)+'\n')

def main():
    total_food = load_pickle("ingredients.pickle")
    # print(len(total_food)) 498
    get_nutrient_raw(total_food[START:])


if __name__== "__main__":
  main()
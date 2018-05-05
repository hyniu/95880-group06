import pickle  
import json
import requests
import csv
import pandas as pd

"""
This file is to scrape recipes and clean raw data. 
"""

FNAME = 'recipe_clean.csv'

def load_pickle(fname):
    """load the pickle file to get all the food.
    Arguments:
        fname {string} -- file to be loaded
    """
    with open(fname, 'rb') as f:
        total_food = pickle.load(f) 
    return total_food

def get_recipe(food):
    """Scrape recipes information for the food.
    Arguments:
        food {string} -- key word to search and scrape
    Returns:
        data {string} - text information of the recipe
    """
    URL = "https://www.themealdb.com/api/json/v1/1/search.php?s=" + food
    response = requests.get(URL)
    data = response.text
    return data

def get_recipe_raw(total_food):
    """Scrape raw data information for the food recipe.
    Arguments:
        food {string} -- key word to search and scrape
    """
    with open("recipe.txt", "w") as f:
        for food in total_food:
            data = get_recipe(food)
            f.write(data+'\n')

def get_recipe_clean(total_food):
    """Get clean data information for the food recipe.
    Arguments:
        total_food  {list of string} -- list of all food
    Returns:
        recipe_dict {dictionary} -- dictionary which stored all clean data of recipe.
    """
    recipe_clean = open(FNAME, 'w')
    csvwriter = csv.writer(recipe_clean)
    head_flag = True
    recipe_dict = {}
    for food in total_food:
        data = get_recipe(food)
        data = json.loads(data)
        if data["meals"] is not None:
            recipe_dict[food] = []
            for item in data["meals"]:
                recipe_dict[food].append(item['idMeal'])
                if head_flag:
                    header = item.keys()
                    csvwriter.writerow(header)
                    head_flag = False
                csvwriter.writerow(item.values())
    recipe_clean.close()
    return recipe_dict

def remove_dup(fname):
    """Remove duplicate rows in the file.
    Arguments:
        fname {string} -- csv filename
    """
    df = pd.read_csv(fname)
    df.set_index("idMeal", inplace=True)
    df = df[~df.index.duplicated(keep='first')]
    df.to_csv(FNAME)

def save_pickle(data, fname):
    """Save data in pickle file.
    Arguments:
        data  -- data to be saved.
        fname {string} -- saved file name
    """
    with open(fname, 'wb') as f:
        pickle.dump(data, f)
    

def main():
    total_food = load_pickle("ingredients.pickle")
    get_recipe_raw(total_food)
    recipe_dict = get_recipe_clean(total_food)
    save_pickle(recipe_dict, "food_to_ids.pickle")
    remove_dup(FNAME)

if __name__== "__main__":
    main()
import pickle  
import json
import requests
import csv
import pandas as pd

FNAME = 'recipe_clean.csv'

def load_pickle(fname):
    with open(fname, 'rb') as f:
        total_food = pickle.load(f) 
    return total_food

def get_recipe(food):
    URL = "https://www.themealdb.com/api/json/v1/1/search.php?s=" + food
    response = requests.get(URL)
    data = response.text
    return data

def get_recipe_raw(total_food):
    with open("recipe.txt", "w") as f:
        for food in total_food:
            data = get_recipe(food)
            f.write(data+'\n')

def get_recipe_clean(total_food):
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
    df = pd.read_csv(fname)
    df.set_index("idMeal", inplace=True)
    df = df[~df.index.duplicated(keep='first')]
    df.to_csv(FNAME)

def save_pickle(data, fname):
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
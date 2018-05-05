import requests
import pickle  
import json  
"""
This file is to scrape all the food names. 
"""
def get_total_food():
    """Scrape and get food names.
    Returns:        
        total_food {list of string} -- all the food names. 
    """
    URL = "https://www.themealdb.com/api/json/v1/1/list.php?i=list"
    response = requests.get(URL)
    data = response.text
    data = json.loads(data)

    total_food = []
    for item in data['meals']:
        total_food.append(item['strIngredient'])
    return total_food

def save_pickle(data, fname):
    """Save the data to pickle.
    Arguments:
        data -- any data to be saved
        fname {string} -- file to be loaded
    """
	with open(fname, 'wb') as f:
		pickle.dump(data, f)

def main():
    total_food = get_total_food()
    save_pickle(total_food, "ingredients.pickle")

if __name__== "__main__":
  main()
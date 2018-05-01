import requests
import pickle  
import json  

def get_total_food():
    URL = "https://www.themealdb.com/api/json/v1/1/list.php?i=list"
    response = requests.get(URL)
    data = response.text
    data = json.loads(data)

    total_food = []
    for item in data['meals']:
        total_food.append(item['strIngredient'])
    return total_food

def save_pickle(data, fname):
	with open(fname, 'wb') as f:
		pickle.dump(data, f)

def main():
    total_food = get_total_food()
    save_pickle(total_food, "ingredients.pickle")

if __name__== "__main__":
  main()
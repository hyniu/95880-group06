import urllib.request
import pandas as pd

RECIPE = pd.read_csv('recipe_clean.csv')

def download_img(url, idMeal):
    filename = 'imgs/' + str(idMeal) + '.jpg'
    print(filename)
    print(url)
    urllib.request.urlretrieve(url,filename)

def main():
    num = len(RECIPE.index)
    for i in range(num):
        data = RECIPE.iloc[[i]].to_dict()
        idMeal = data['idMeal'][i]
        url = data['strMealThumb'][i]
        download_img(url, idMeal)


if __name__== "__main__":
    main()
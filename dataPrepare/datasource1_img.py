import urllib.request
import pandas as pd
"""
This file is to scrape images of meals. 
"""

RECIPE = pd.read_csv('recipe_clean.csv')

def download_img(url, idMeal):
    """Download and save images to the foloder.
    Arguments:
        url {string} -- url of image to be downloaded
        idMeal {string} -- corresponding idMeal
    """
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
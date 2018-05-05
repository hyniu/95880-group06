from easygui import *
import os
import pandas as pd
import pickle


original_nutrient = {}
selected_nutrient = {}
recipe_nutrient = {}
selected_recipes = []
s_calories = 0 # a global
s_sodium =0 # a global
s_dietary_fiber=0 # a global
s_protein=0 # a global
s_vitamin_a_dv=0 # a global
s_vitamin_c_dv =0 # a global
s_calcium_dv =0 # a global
s_iron_dv=0 # a global

food_list = ['Aubergine', 'Avocado', 'Beef', 'Beef Brisket', 
            'Bread', 'Broccoli', 'Butter', 'Cajun', 'Cheese', 
            'Chicken', 'Chickpeas', 'Chilli', 'Christmas Pudding', 
            'Cream', 'Cumin', 'Fennel', 'French Lentils', 'Garlic', 
            'Honey', 'Lamb', 'Leek', 'Lime', 'Mustard', 'Peanut Butter', 
            'Peas', 'Pine Nuts', 'Pork', 'Potatoes', 'Rice', 'Rigatoni', 
            'Sage', 'Salmon', 'Salt', 'Spaghetti', 'Spinach', 'Squash', 
            'Sugar', 'Thyme', 'Tuna', 'Yogurt', 'Cream Cheese', 'Caramel', 
            'Onion', 'Tomato', 'Duck', 'Couscous', 'Minced Beef', 'Ricotta', 
            'Banana', 'Pumpkin', 'Paneer', 'Lentils', 'Tahini', 'Ham', 'Treacle',
            'Egg', 'Prosciutto', 'Brie', 'White Chocolate', 'Ackee', 'Jerk', 
            'Oxtail', 'Broad Beans']




# -----------------------------------------------------------------------
#          Load data 
#-----------------------------------------------------------------------
def load_pickle(fname):
    with open(fname, 'rb') as f:
        total_food = pickle.load(f) 
    # to lower case
    total_food = {k.lower(): v for k, v in total_food.items()}
    return total_food

FOOD_TO_IDS = load_pickle("dataFiles/food_to_ids.pickle")
RECIPE = pd.read_csv('dataFiles/recipe_clean.csv').fillna(0)
RECIPE.set_index("idMeal", inplace=True)
INGRED = pd.read_csv('dataFiles/ingredient_clean.csv').fillna(0)
INGRED.set_index("key_ingredient", inplace=True)
NUNEED = pd.read_csv('dataFiles/nutrient_need_clean.csv').fillna(0)



# -----------------------------------------------------------------------
#          Get recipe list 
#-----------------------------------------------------------------------
def get_recipe_list(food):
    if food.title() in food_list:
        ids = FOOD_TO_IDS[food.lower()]
        ids = [int(x) for x in ids]
        return RECIPE.loc[ids]
    else:
        return None

 
# -----------------------------------------------------------------------
#          Get nutrient user need 
#-----------------------------------------------------------------------   
def get_nutrient_need(age, gender):
    idx = int(age) - 1
    if gender.lower() == 'm' or "male":
        idx += 100
    return NUNEED.iloc[idx].to_dict()



# -----------------------------------------------------------------------
#          Get user's basic information
#-----------------------------------------------------------------------
def get_user_info():
    while True:
        msg = "Enter your personal information"
        title = "Personal Information"
        fieldNames = ["Gender:F/M", "Age"]
        Entervalue = multenterbox(msg, title, fieldNames)
        valid_input=["f","m","male","female"]
        if Entervalue[1].isdigit() and Entervalue[0].lower() in valid_input:
            return Entervalue
        else:
            msgbox("Invalid input! please try again.", "Notice")
    


# -----------------------------------------------------------------------
#          Get start to the program, initial the home page
#-----------------------------------------------------------------------
def getStart():
    
    Entervalue = get_user_info()

    original_nutrient = get_nutrient_need(Entervalue[1], Entervalue[0])
   
    choices = ["Search for recipes",
                "View selected recipes"]
   
    while True:
        msg = "Your Gender is: {},\nYour age is: {}\nHere are nutrient facts you need per day:"\
            .format(original_nutrient['gender'], original_nutrient['age'])

        nutrient_detail = "\nProtein: {:.2f}/{} g/day\nFiber: {:.2f}/{} g/day\nVitamin A: {:.2f}/{} g/day\n"\
            "Vitamin C: {:.2f}/{} mg/day\nCalcium: {:.2f}/{} mg/day\nIron: {:.2f}/{} mg/day\nSodium: {:.2f}/{}  mg/day"\
            .format(int(s_protein),original_nutrient['Protein\tg/day'],int(s_dietary_fiber),original_nutrient['Fibre\tg/day'],\
            int(s_vitamin_a_dv),original_nutrient['Vitamin A\t_g/day'],int(s_vitamin_c_dv),original_nutrient['Vitamin C\tmg/day'],\
            int(s_calcium_dv),original_nutrient['Calcium\tmg/day'],int(s_iron_dv),original_nutrient['Iron\tmg/day'],\
            int(s_sodium),original_nutrient['Sodium\tmg/day'])

        choice = choicebox(msg+nutrient_detail, "GetNutrient", choices)
        if not choice: return
        if choice == 'Search for recipes':
            searchForRecipes()
        if choice == 'View selected recipes':
            viewSelected()
        	


# -----------------------------------------------------------------------
#          Search for recipes based on user's input
#          Calculate nutrient facts for selected recipe
#          Update user's selected nutrient facts 
#-----------------------------------------------------------------------
def searchForRecipes():

    #Search for recipes based on user's input
    SearchedFood = multenterbox("Please enter the food you want to cook", "Find recipes", ["Food name"])
    if SearchedFood is None:
        return 
    if get_recipe_list(SearchedFood[0]) is None:
        msgbox("Opps! We don't have this food, try another :)", "Notice")
        return
    
    all_recipe = get_recipe_list(SearchedFood[0])
    recipeList=[]
    idList= []

    num = len(all_recipe.index)
    for i in range(num):
        data = all_recipe.iloc[[i]].to_dict()
        name_dict = data['strMeal']
        idMeal = list(name_dict.keys())[0]
        name = list(name_dict.values())[0]

        # get all recipes's names 
        recipeList.append(name)

        # get all recipes's ids
        idList.append(idMeal)
    
    # Show all recipes that satisfies user's input
    recipe_choice = choicebox("Here are recipes contains "+SearchedFood[0], "Recipe List", recipeList)
    all_ingredients = {}

    # Show details based on user's selection
    # Calculate nutrient facts for this recipe
    for i in range(len(recipeList)):
        if recipe_choice==recipeList[i]:
            data = all_recipe.iloc[[i]].to_dict()
            instruction = list(data['strInstructions'].values())[0]
            idMeal = idList[i]

            nf_calories =0
            nf_sodium =0
            nf_dietary_fiber=0
            nf_protein=0
            nf_vitamin_a_dv=0
            nf_vitamin_c_dv =0
            nf_calcium_dv =0
            nf_iron_dv=0
            

            # find ingredinets and measurement from recipe
            for j in range(1,20):
                ingredient = "strIngredient"+str(j)
                measure = "strMeasure"+str(j)
                food = list(data[ingredient].values())[0]
               
                #search each ingredient, and return nutrient
                if isinstance(food, str):
                    index_set = set(INGRED.index)

                    if food in index_set:
                        # calculate total nutrient facts this recipe has
                        try:
                            a = INGRED.loc[food.title()]
                            nf_calories += float(a['nf_calories'])
                            nf_sodium += float(a['nf_sodium'])
                            nf_dietary_fiber+=float(a['nf_dietary_fiber'])
                            nf_protein+=float(a['nf_protein'])
                            nf_vitamin_a_dv+=float(a['nf_vitamin_a_dv'])
                            nf_vitamin_c_dv +=float(a['nf_vitamin_c_dv'])
                            nf_calcium_dv +=float(a['nf_calcium_dv'])
                            nf_iron_dv+=float(a['nf_iron_dv'])

                            # get image of this recipe
                            image = 'imgs/'+str(idMeal)+'.jpg'
                            instruction = "Here are nutrient facts this meal contains:\nCalories: {:.2f}\nSodium: {:.2f}\n"\
                                "Fiber: {:.2f}\nProtein: {:.2f}\nVitamin A: {:.2f}\nVitamin C: {:.2f}\nCalcium: {:.2f}\nIron: {:.2f}\n\nInstruction:\n{}".\
                                format(nf_calories,nf_sodium,nf_dietary_fiber,nf_protein,nf_vitamin_a_dv,nf_vitamin_c_dv,\
                                    nf_calcium_dv,nf_iron_dv,instruction)
                            yn = buttonbox(instruction, "Recipes", ['Cancel', 'Select'], image=image)
                        except:
                            yn = buttonbox(instruction, "Recipes", ['Cancel', 'Select'], image=image)
                        finally:
                            if yn == 'Select':
                                # if user select this recipe, add this recipe to selected list
                                selected_recipes.append(recipeList[i])
                                global s_calories 
                                global s_sodium 
                                global s_dietary_fiber
                                global s_protein
                                global s_vitamin_a_dv
                                global s_vitamin_c_dv 
                                global s_calcium_dv 
                                global s_iron_dv
                                
                                # add update nutrient facts this user intake
                                s_calories += nf_calories
                                s_sodium += nf_sodium
                                s_dietary_fiber += nf_dietary_fiber
                                s_protein += nf_protein
                                s_vitamin_a_dv+= nf_vitamin_a_dv
                                s_vitamin_c_dv += nf_vitamin_c_dv
                                s_calcium_dv +=nf_calcium_dv
                                s_iron_dv+=nf_iron_dv

                                msgbox(recipeList[i]+" has been added", "Add Successfully")
                                return 


# -----------------------------------------------------------------------
#          View selected recipes
#-----------------------------------------------------------------------
def viewSelected():
    content = ""
    for r in selected_recipes:
        content += r+"\n"
    textbox("Here Are Recipes You Have Selected","Recipes",content) 



# -----------------------------------------------------------------------
#          Main 
#-----------------------------------------------------------------------
def main():
    getStart()



if __name__ == "__main__":
    main()


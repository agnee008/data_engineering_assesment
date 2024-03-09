import json
import requests
import unittest

def fetch_recipes(url):
    """
    Fetches recipes from the provided URL.

    Args:
        url (str): The URL from which to fetch recipes.

    Returns:
        list: A list of dictionaries representing the fetched recipes.
    """
    response = requests.get(url)
    data = response.text.split('\n')
    recipes = [json.loads(recipe) for recipe in data if recipe.strip()]
    return recipes

def extract_chili_recipes(recipes):
    """
    Extracts chili recipes from a list of recipes.

    Args:
        recipes (list): A list of dictionaries representing recipes.

    Returns:
        list: A list of dictionaries representing chili recipes.
    """
    chili_recipes = []
    for recipe in recipes:
        ingredients = recipe['ingredients'].lower()
        if 'chili' in ingredients or 'chiles' in ingredients:
            total_time = get_total_time(recipe)
            print(f"Total Time for {recipe['name']}: {total_time} minutes")
            recipe['difficulty'] = assess_difficulty(recipe)
            chili_recipes.append(recipe)
    return chili_recipes

def assess_difficulty(recipe):
    """
    Assesses the difficulty level of a recipe based on total preparation and cooking time.

    Args:
        recipe (dict): A dictionary representing a recipe.

    Returns:
        str: The difficulty level of the recipe ('Easy', 'Medium', 'Hard', or 'Unknown').
    """
    total_time = get_total_time(recipe)
    print(f"Total Time: {total_time}")
    if total_time < 30:
        return 'Easy'   
    elif total_time <= 60:
        return 'Medium'
    elif total_time > 60:
        return 'Hard'
    else:
        return 'Unknown'

def get_total_time(recipe):
    """
    Calculates the total preparation and cooking time of a recipe in minutes.

    Args:
        recipe (dict): A dictionary representing a recipe.

    Returns:
        int: The total preparation and cooking time of the recipe in minutes, or None if time data is missing.
    """
    prep_time = parse_time(recipe.get('prepTime', ''))
    cook_time = parse_time(recipe.get('cookTime', ''))
    if prep_time is None or cook_time is None:
        return None
    return prep_time + cook_time

def parse_time(time_str):
    """
    Parses a time string and returns the time in minutes.

    Args:
        time_str (str): A string representing a time duration in ISO 8601 format.

    Returns:
        int: The time duration in minutes.
    """
    if 'PT' not in time_str:
        return 0
    
    time_str = time_str.replace('PT', '')
    time_str = time_str.replace('H', 'H ')
    time_str = time_str.replace('M', 'M ')
    time_components = time_str.split()

    hours = 0
    minutes = 0
    for component in time_components:
        if 'H' in component:
            hours = int(component[:-1])
        elif 'M' in component:
            minutes = int(component[:-1])
    
    return hours * 60 + minutes

def save_chili_results(chili_recipes, file_path):
    """
    Saves chili recipes to a CSV file.

    Args:
        chili_recipes (list): A list of dictionaries representing chili recipes.
        file_path (str): The path to the CSV file where recipes will be saved.
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('name|ingredients|url|image|cookTime|recipeYield|datePublished|prepTime|description|difficulty\n')
        for recipe in chili_recipes:
            f.write(f"{recipe['name']}|{recipe['ingredients']}|{recipe['url']}|{recipe['image']}|{recipe['cookTime']}|{recipe['recipeYield']}|{recipe['datePublished']}|{recipe['prepTime']}|{recipe['description']}|{recipe['difficulty']}\n")

def calculate_average_time(difficulty_levels, file_path):
    """
    Calculates the average total time for each difficulty level and saves the results to a CSV file.

    Args:
        difficulty_levels (dict): A dictionary containing lists of recipes categorized by difficulty level.
        file_path (str): The path to the CSV file where the average times will be saved.
    """
    with open(file_path, 'w') as f:
        f.write("Difficulty|AverageTotalTime\n")
        for level, recipes in difficulty_levels.items():
            total_time = sum([parse_time(recipe['prepTime']) + parse_time(recipe['cookTime']) for recipe in recipes])
            avg_time = total_time // len(recipes) if len(recipes) > 0 else 0
            f.write(f"{level}|{avg_time}\n")

class TestRecipeFunctions(unittest.TestCase):
    def test_fetch_recipes(self):
        """
        Test the fetch_recipes function.
        """
        url = 'https://bnlf-tests.s3.eu-central-1.amazonaws.com/recipes.json'
        recipes = fetch_recipes(url)
        self.assertTrue(isinstance(recipes, list))
        self.assertTrue(len(recipes) > 0)
    
    def test_extract_chili_recipes(self):
        """
        Test the extract_chili_recipes function.
        """
        recipe = {
            'name': 'Chili Con Carne',
            'ingredients': 'ground beef, chili powder, beans',
            'prepTime': 'PT30M',
            'cookTime': 'PT1H',
            'difficulty': 'Unknown'
        }

        extracted_recipes = extract_chili_recipes([recipe])
        self.assertTrue(isinstance(extracted_recipes, list))
        self.assertTrue(len(extracted_recipes) > 0)
        self.assertEqual(extracted_recipes[0]['difficulty'], 'Hard')
    
    def test_parse_time(self):
        """
        Test the parse_time function.
        """
        time_str = 'PT1H30M'
        time_in_minutes = parse_time(time_str)
        self.assertEqual(time_in_minutes, 90)

        time_str = 'PT45M'
        time_in_minutes = parse_time(time_str)
        self.assertEqual(time_in_minutes, 45)
    
    def test_easter_leftover_sandwich_not_chili(self):
        """
        Test that the Easter Leftover Sandwich is not considered a chili recipe.
        """
        recipe = {
            "name": "Easter Leftover Sandwich",
            "ingredients": "12 whole Hard Boiled Eggs\n1/2 cup Mayonnaise\n3 Tablespoons Grainy Dijon Mustard\n Salt And Pepper, to taste\n Several Dashes Worcestershire Sauce\n Leftover Baked Ham, Sliced\n Kaiser Rolls Or Other Bread\n Extra Mayonnaise And Dijon, For Spreading\n Swiss Cheese Or Other Cheese Slices\n Thinly Sliced Red Onion\n Avocado Slices\n Sliced Tomatoes\n Lettuce, Spinach, Or Arugula",
            "url": "http://thepioneerwoman.com/cooking/2013/04/easter-leftover-sandwich/",
            "image": "http://static.thepioneerwoman.com/cooking/files/2013/03/leftoversandwich.jpg",
            "cookTime": "PT",
            "recipeYield": "8",
            "datePublished": "2013-04-01",
            "prepTime": "PT15M",
            "description": "Got leftover Easter eggs?    Got leftover Easter ham?    Got a hearty appetite?    Good! You've come to the right place!    I..."
        }

        extracted_recipes = extract_chili_recipes([recipe])
        self.assertEqual(len(extracted_recipes), 0, "Easter Leftover Sandwich should not be considered a chili recipe")

if __name__ == '__main__':
    unittest.main()

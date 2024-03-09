import json
import requests

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
    recipes = [json.loads(recipe) for recipe in data if recipe.strip()]  # used list comprehension with nullyfying the space
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
            recipe['difficulty'] = assess_difficulty(recipe)
            chili_recipes.append(recipe)
    return chili_recipes

def assess_difficulty(recipe):
    """
    Assesses the difficulty level of a recipe based on total preparation and cooking time.

    Args:
        recipe (dict): A dictionary representing a recipe.

    Returns:
        str: The difficulty level of the recipe ('Easy', 'Medium', 'Hard', 'Unknown').
    """
    total_time = get_total_time(recipe)
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
    prep_time = parse_time(recipe['prepTime'])
    cook_time = parse_time(recipe['cookTime'])
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
    Saves unique chili recipes to a CSV file.

    Args:
        chili_recipes (list): A list of dictionaries representing chili recipes.
        file_path (str): The path to the CSV file where recipes will be saved.
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('name|ingredients|url|image|cookTime|recipeYield|datePublished|prepTime|description|difficulty\n')
        saved_recipes = set()
        for recipe in chili_recipes:
            recipe_key = (recipe['name'], recipe['ingredients'], recipe['url'])  # checking if the recipe has been saved already based on a combination of name, ingredients, and URL
            if recipe_key not in saved_recipes:
                f.write(f"{recipe['name']}|{recipe['ingredients']}|{recipe['url']}|{recipe['image']}|{recipe['cookTime']}|{recipe['recipeYield']}|{recipe['datePublished']}|{recipe['prepTime']}|{recipe['description']}|{recipe['difficulty']}\n")
                saved_recipes.add(recipe_key)
        print(f"Unique chili recipes saved to {file_path}")


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
    print(f"Average times calculated and saved to {file_path}")

def main():
    """
    Main function to fetch, extract, save, and analyze chili recipes.
    """
    url = 'https://bnlf-tests.s3.eu-central-1.amazonaws.com/recipes.json'
    print("***Fetching recipes***")
    recipes = fetch_recipes(url)
    print(f"Fetched {len(recipes)} recipes")
    chili_recipes = extract_chili_recipes(recipes)
    print(f"Extracted {len(chili_recipes)} chili recipes")
    save_chili_results(chili_recipes, 'output_data/Chilies.csv')
    difficulty_levels = {'Easy': [], 'Medium': [], 'Hard': []}
    for recipe in chili_recipes:
        difficulty_levels[recipe['difficulty']].append(recipe)
    calculate_average_time(difficulty_levels, 'output_data/Results.csv')

if __name__ == '__main__':
    main()

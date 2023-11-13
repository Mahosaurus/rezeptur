import json
import os
import random

from flask import current_app as app
from flask import request, redirect, flash, render_template, url_for, send_from_directory
from src.data_storage.postgres_handler import PostgresInteraction

postgres_conn = PostgresInteraction(app.config["POSTGRES_HOST"],
                                    app.config["POSTGRES_DBNAME"],
                                    app.config["POSTGRES_USER"],
                                    app.config["POSTGRES_PASSWORD"],
                                    app.config["POSTGRES_TABLE"])


# Sample recipe data (you can replace this with a database later)
@app.route(f'/{app.config["SECRET_KEY"]}', methods=['GET'])
def index():
    # Query the database for all recipes
    recipes = postgres_conn.extract_data_from_postgres() # recipe 1, recipe 2
    # Get the unique courses for the filter options
    courses = set(recipe['course'] for recipe in recipes) # starter, main...
    return render_template('index.html', random_recipe=None, courses=courses, recipes=recipes)

@app.route('/single_random_recipe', methods=['GET','POST'])
def single_random_recipe():
    # Query the database for all recipes
    recipes = postgres_conn.extract_data_from_postgres()
    if request.method == 'GET':
        return redirect(url_for('index'))

    course = request.form.get('course')

    # Get a list of recipes for the selected course
    course_recipes = [recipe for recipe in recipes if recipe['course'] == course]
    if not course_recipes:
        return redirect(url_for('index'))

    random_recipe = random.choice(course_recipes)

    # Add hyperlink to source
    source = random_recipe["source"]
    random_recipe["source"] = f"<a href='{source}'>{source}</a>"
    print(random_recipe["source"])
    return render_template('index.html', random_recipe=random_recipe, recipes=recipes)

@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        # Handle form submission and add the new recipe to the data structure
        new_recipe = {
            "name": request.form['name'],
            "course": request.form['course'],
            "description": request.form['description'],
            "source": request.form['source'],
            "season": request.form['season'],
            "style": request.form['style']
        }
        postgres_conn.send_data_to_postgres(new_recipe)
        return "Recipe added successfully!"

    # If it's a GET request, just render the form
    recipes = postgres_conn.extract_data_from_postgres()
    return render_template('add_recipe.html', courses=set(recipe['course'] for recipe in recipes))

@app.route('/export_data', methods=['POST'])
def export_data():
    recipes = postgres_conn.export_database()
    # Return recipes as a file to download, do not render a template, do not return a str
    with open(os.path.join(app.root_path, 'recipes.txt'), 'w') as f:
        json.dump(recipes, f, indent=4)
    return send_from_directory(app.root_path, 'recipes.txt')

import random

from flask import current_app as app
from flask import request, redirect, flash, render_template, url_for
from src.data_storage.postgres_handler import extract_data_from_postgres, send_data_to_postgres

# Sample recipe data (you can replace this with a database later)
@app.route('/')
def index():
    # Query the database for all recipes
    recipes = extract_data_from_postgres(app.config["POSTGRES_HOST"],
                                         app.config["POSTGRES_DBNAME"],
                                         app.config["POSTGRES_USER"],
                                         app.config["POSTGRES_PASSWORD"])
    # Get the unique courses for the filter options
    courses = set(recipe['course'] for recipe in recipes)
    return render_template('index.html', random_recipe=None, courses=courses, recipes=recipes)

@app.route('/single_random_recipe', methods=['GET','POST'])
def single_random_recipe():
    # Query the database for all recipes
    recipes = extract_data_from_postgres(app.config["POSTGRES_HOST"],
                                         app.config["POSTGRES_DBNAME"],
                                         app.config["POSTGRES_USER"],
                                         app.config["POSTGRES_PASSWORD"])
    if request.method == 'GET':
        return redirect(url_for('index'))

    course = request.form.get('course')

    # Get a list of recipes for the selected course
    course_recipes = [recipe for recipe in recipes if recipe['course'] == course]
    if not course_recipes:
        return redirect(url_for('index'))

    random_recipe = random.choice(course_recipes)
    random_recipe.pop('id')
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
        send_data_to_postgres(app.config["POSTGRES_HOST"],
                              app.config["POSTGRES_DBNAME"],
                              app.config["POSTGRES_USER"],
                              app.config["POSTGRES_PASSWORD"],
                              new_recipe)
        return "Recipe added successfully!"

    # If it's a GET request, just render the form
    return render_template('add_recipe.html', courses=set(recipe['course'] for recipe in recipes))

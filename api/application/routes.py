from flask import current_app as app
from flask import request, redirect, flash, render_template

# Sample recipe data (you can replace this with a database later)
recipes = [
    { "name": "Recipe 1", "course": "starter", "source": "https://www.google.de", "season": "", "style": ""},
    { "name": "Recipe 3", "course": "starter", "source": "Buch", "season": "", "style": "" },
    { "name": "Recipe 2", "course": "main", "source": "Kopf", "season": "", "style": "" },
    # Add more recipes here...
]

@app.route('/')
def index():
    # Get the unique courses for the filter options
    courses = set(recipe['course'] for recipe in recipes)
    return render_template('index.html', courses=courses, recipes=recipes)

@app.route('/random_recipe', methods=['POST'])
def random_recipe():
    course = request.form.get('course')
    # Get a list of recipes for the selected course
    course_recipes = [recipe for recipe in recipes if recipe['course'] == course]
    if not course_recipes:
        return "No recipes found for the selected course."

    random_recipe = random.choice(course_recipes)
    return render_template('random_recipe.html', random_recipe=random_recipe)

@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        # Handle form submission and add the new recipe to the data structure
        new_recipe = {
            "name": request.form['name'],
            "course": request.form['course'],
            "ingredients": request.form['ingredients'],
            "instructions": request.form['instructions']
        }
        recipes.append(new_recipe)
        return "Recipe added successfully!"

    # If it's a GET request, just render the form
    return render_template('add_recipe.html', courses=set(recipe['course'] for recipe in recipes))

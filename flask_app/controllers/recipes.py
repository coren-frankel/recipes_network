from flask import render_template, redirect, request, session, flash, url_for
from flask_app import app
from flask_app.models.recipe import Recipe
from flask_app.models.user import User

@app.route('/recipes/new')
def display_recipe_form():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('new_recipe.html')

@app.route('/recipes/create', methods=['POST'])
def submit_recipe():
    if not Recipe.validate_recipe(request.form):
        # temp = {
        #     "name" : request.form['name'],
        #     "description" : request.form['description'],
        #     "instructions" : request.form['instructions']
        # }
        return render_template('new_recipe.html')#, temp=temp)
    data = {
        "user_id" : session['user_id'],
        "name" : request.form['name'].title(),
        "under_30" : request.form['under_30'],
        "description" : request.form['description'],
        "instructions" : request.form['instructions'],
        "date_made" : request.form['date_made']
    }
    print(data)
    Recipe.submit(data)
    return redirect('/recipes')


@app.route('/edit/<int:rcp_id>')
def edit_recipe(rcp_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id" : rcp_id,
    }
    recipe = Recipe.grab_recipe(data)
    if recipe['user_id'] != session['user_id']:
        return redirect('/')
    return render_template('edit_recipe.html', recipe = recipe)

@app.route('/recipes/<int:rcp_id>')
def display_recipe(rcp_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id" : rcp_id,
    }
    user_data = {
        "id" : session['user_id']
    }
    return render_template('show_recipe.html', 
    recipe = Recipe.grab_recipe(data), user = User.get_by_id(user_data))

@app.route('/delete/<int:rcp_id>')
def delete_message(rcp_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id" : rcp_id
    }
    recipe = Recipe.grab_recipe(data)
    if recipe['user_id'] != session['user_id']:
        return redirect('/')
    Recipe.delete_recipe(data)
    return redirect('/recipes')

if __name__ == "__main__":
    app.run(debug=True)
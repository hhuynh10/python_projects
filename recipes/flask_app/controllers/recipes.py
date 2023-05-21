from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import recipe
from flask_app.models import user

@app.route('/recipes')
def recipes():
    if 'user_id' not in session:
        return redirect ('/users/logout')
    this_user = user.User.get_user_by_id(session['user_id'])
    return render_template ('recipes.html', this_user = this_user, recipes = recipe.Recipe.view_all_recipes())

@app.route('/recipes/new')
def new_recipe():
    if 'user_id' not in session:
        return redirect ('/users/logout')
    this_user = user.User.get_user_by_id(session['user_id'])
    return render_template('new_recipe.html', this_user = this_user)

@app.route('/recipes/add', methods = ['POST'])
def add_recipes():
    if recipe.Recipe.create_recipe(request.form):
        return redirect ('/recipes')
    return redirect ('/recipes/new')

@app.route('/delete/<int:id>')
def delete(id):
    recipe.Recipe.delete_recipe(id)
    return redirect ('/recipes')

@app.route('/recipes/edit/<int:id>')
def edit(id):
    if 'user_id' not in session:
        return redirect ('/users/logout')
    this_user = user.User.get_user_by_id(session['user_id'])
    return render_template('edit_recipe.html', this_user = this_user, recipe = recipe.Recipe.view_one_recipe(id))

@app.route('/recipes/edit', methods=['POST'])
def edit_recipe():
    id = request.form['id']
    if not recipe.Recipe.validate_rep_data(request.form):
        return redirect (f"/recipes/edit/{id}")
    recipe.Recipe.update_recipe(request.form)
    return redirect ('/recipes')

@app.route('/recipes/<int:id>')
def view_recipe(id):
    if 'user_id' not in session:
        return redirect ('/users/logout')
    this_user = user.User.get_user_by_id(session['user_id'])
    return render_template('view_recipe.html', this_user = this_user, recipe = recipe.Recipe.view_one_recipe(id))

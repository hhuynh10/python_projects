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
        return redirect ('/logout')
    this_user = user.User.get_user_by_id(session['user_id'])
    return render_template('new_recipe.html', this_user = this_user)

@app.route('/recipes/add', methods = ['POST'])
def add_recipes():
    if recipe.Recipe.create_recipe(request.form):
        return redirect ('/recipes')
    return redirect ('/recipes/new')
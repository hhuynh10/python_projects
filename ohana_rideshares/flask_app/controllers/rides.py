from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import ride
from flask_app.models import user


@app.route('/rides/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect ('/users/logout')
    this_user = user.User.get_user_by_id(session['user_id'])
    return render_template ('dashboard.html', this_user = this_user, rides = ride.Ride.get_all())

@app.route('/rides/new')
def new_ride():
    if 'user_id' not in session:
        return redirect ('/users/logout')
    this_user = user.User.get_user_by_id(session['user_id'])
    return render_template('new_ride.html', this_user = this_user)

@app.route('/rides/add', methods = ['POST'])
def add_ride():
    if ride.Ride.request_ride(request.form) :
        return redirect ('/rides/dashboard')
    return redirect ('/rides/new')
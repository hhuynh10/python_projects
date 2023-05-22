from flask import Flask, render_template, redirect, request
from flask_app import app
from flask_app.models.interest import Interest
from flask_app.models.ninja import Ninja

'''READ'''
@app.route('/read/interests')
def read_interests():
    return render_template("read_interests.html", output = Interest.select_all())
    # 1) select * interests

@app.route('/read/interest/<interest_id>')
def read_one(interest_id):
    data={"interest_id": interest_id}
    # 1) get interest id from url
    return render_template( "read_interest.html", output=Interest.select_one(data), elements=Ninja.select_all() )
    # 2) save interest class data = output
    # 3) show all ninjas as classes for form select = elements

'''CREATE'''
@app.route("/process/interest", methods=["post"])
def process_interest():
    data=request.form
    # 1) get name and descriotion frm form
    Interest.insert(data)
    # 2) insert into interests(name, description) VALUES(data)
    return redirect("/read/interests")

@app.route("/process/ninjas_interest", methods=["POST"])
def process_ninjas_interests():
    data=request.form
    # 1) get form data values(ninja_id, interest_id)
    Interest.insert_ninjas_interests(data)
    # 2) insert into ninjas_interests values(data)
    return redirect(f"/read/interest/{data['interest_id']}")


'''UPDATE'''
@app.route("/change/interest", methods=["post"])
def change_interest():
    data=request.form
    # 1) get id, name, description from form
    Interest.update(data)
    # 2) update interests values(data) where id=data['id']
    return redirect(f"/read/interest/{data['id']}")


'''DELETE'''
@app.route("/delete/ninjas_interests/<interest_id>/<ninja_id>")
def delete_ninjas_interests(interest_id, ninja_id):
    data={"id" : ninja_id}
    Interest.delete_interest_ninja(data)
    return redirect(f"/read/interest/{interest_id}")

@app.route("/delete/interest/<id>")
def delete(id):
    data={"id":id}
    Interest.delete(data)
    return redirect("/read/interests")
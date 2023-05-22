from flask import Flask, render_template, request, redirect
# 1) import extentions
from flask_app import app
from flask_app.models.interest import Interest
# 2) import application
from flask_app.models.ninja import Ninja
from flask_app.models.dojo import Dojo
from flask_app.models.address import Address
# 3) import models

'''INDEX'''
@app.route('/')
def index():
    return render_template("index.html")


'''READ ALL'''
@app.route('/read/ninjas')
def read_all():
    return render_template("read_ninjas.html", output = Ninja.select_all(), get=Dojo.select_all())

'''READ ONE'''
@app.route("/read/ninja/<id>")
def read_ninja(id):
# 1) take in id parameter
    data={"id": id}
    # 2) save to data dict
    return render_template("read_ninja.html", output = Ninja.select_one(data),  elements = Interest.get_interests(data), get = Dojo.select_all())
    # 3) output = one ninja
    # 3) elements = get interests
    # 3) get dojos for select

'''CREATE'''
@app.route("/process/ninja", methods=["POST"])
def create_ninja():
    address = {k:v for k,v in request.form.items() if k != "name" and k !="dojo_id"}
    # address = {'address': 't', 'city': 't', 'state': 'tt', 'zip': '00000'}
    # 1) generate address information dictionary
    data = {k:v for k,v in request.form.items() if k=="name" or k=="dojo_id"}
    # data = {'name': 't', 'dojo': '1'}
    # 2) generate ninja data
    data["address_id"] = Address.insert(address)
    # 3) insert into addresses id value(address)
    # 3) save the address id from insert
    # 3) USE AS FOREIN KEY FOR NINJA DATA
    Ninja.insert(data)
    # 4) insert values(name, dojo_id, address_id)
    return redirect("/read/ninjas")

'''UPDATE'''
@app.route("/change/ninja", methods=["POST"])
def change_ninja():
    address = {
    # 1) get address from form
        "address_id": request.form["address_id"],
        "street": request.form["street"],
        "city": request.form["city"],
        "state": request.form["state"],
        "zip": request.form["zip"]
    }
    data={
    # 2) get ninja info from form
        "id": request.form["id"],
        "name": request.form["name"],
        "dojo_id": request.form["dojo_id"]
    }
    Address.update(address)
    # 3) address and dojo are foregn keys
    # 3) good practice to do those first
    # 3) cannot be updated at the same time
    Ninja.update_ninja(data)
    # 4) update ninjas set name, dojo_id WHERE id=data['id']
    return redirect(f"/read/ninja/{data['id']}")

'''DELETE'''
@app.route("/delete/ninja/<id>/<address_id>")
def delete_ninja(id, address_id):
    data={"id":id, "address_id":address_id}
    Ninja.delete(data)
    Address.delete(data)
    return redirect("/read/ninjas")

'''CATCHALL'''
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch(path):
    return render_template("catchall.html")
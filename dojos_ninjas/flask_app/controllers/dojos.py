from flask import Flask, render_template, request, redirect
from flask_app import app
from flask_app.models.dojo import Dojo
from flask_app.models.dojo import Address


'''READ'''
@app.route('/read/dojos')
def read_dojos(): 
    return render_template("read_dojos.html", output = Dojo.select_all())

@app.route("/read/dojo/<id>")
def read_dojo(id):
    data = {"id": id}
    return render_template("read_dojo.html", output=Dojo.select_one(data))

'''CREATE'''
@app.route('/process_new/dojo', methods=["POST"])
def procees_new_dojo():
    address={k:v for k,v in request.form.items() if k != 'name'}
    new = Dojo.insert_address(address)
    # 1) get all form information that isn't dojo name
    # 1) use the form to create a dictionary
    # 1) use address dict to insert address
    data = {'name':request.form["name"]}
    # 2) get name
    data['address_id'] = new
    # 2) get address id from #1
    Dojo.insert(data)
    # 3) insert dojo with data dictionary
    return redirect("/read/dojos")

'''UPDATE'''
@app.route("/change/dojo", methods=["POST"])
def change_dojo():
    address={k:v for k,v in request.form.items() if k !="name" and k !="id"}
    # 1) get address info from form
    data = {"name":request.form["name"], "id":request.form["id"]}
    # 2) get dojo name and id from form
    Dojo.update_address(address)
    # 3) update address using address_id from form and inputs from form
    Dojo.update(data)
    # 4) update ninja name
    # 4) don't need to update address id,
    #       just changed it in step 3
    return redirect(f"/read/dojo/{data['id']}")

@app.route("/delete/dojo/<id>/<address_id>")
def delete_dojo(id, address_id):
    data={"id":id, "address_id":address_id}
    Dojo.delete(data)
    Address.delete(data)
    return redirect("/read/dojos")
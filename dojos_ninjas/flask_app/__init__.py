from flask import Flask
# 1) import flask object

app = Flask(__name__)
# 2) create new app instance from flask object

app.secret_key = "xtina.codes"
# 3) create a secret key
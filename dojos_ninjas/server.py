from flask_app import app
# 1) import application

from flask_app.controllers import ninjas
from flask_app.controllers import dojos
from flask_app.controllers import interests
# 2) import routes

if __name__ == "__main__":
    app.run(debug=True)
# 3) if in file run
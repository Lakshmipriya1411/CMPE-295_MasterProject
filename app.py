from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flasgger import Swagger
from api.database.db import initialize_db
import os
from api.resources.errors  import errors
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/api/": {"origins": "http:///54.153.46.53:5000/"}})
#app.config.from_pyfile('config.py')
swagger = Swagger(app)
mail = Mail(app)
#print(os.environ['JWT_SECRET_KEY'])
#app.config['JWT_SECRET_KEY'] =  os.environ['JWT_SECRET_KEY']
from flask_restful import Api
api = Api(app, errors=errors)
bcrypt = Bcrypt(app)
app.config["JWT_SECRET_KEY"] = "t1NP63m4wnBg6nyHYKfmc2TpCOGI4nss"
jwt = JWTManager(app)
ma = Marshmallow(app)
# imports requiring app and mail
from api.resources.routes import initialize_routes

#initialize_db(app)
initialize_routes(api)




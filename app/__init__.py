from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_jwt_extended import JWTManager
import logging

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = 't1NP63m4wnBg6nyHYKfmc2TpCOGI4nss'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///caycom.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'False'
logging.basicConfig(filename='demo.log', level=logging.DEBUG)
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)
jwt = JWTManager(app)

from app import model, schema, resource, error_handler

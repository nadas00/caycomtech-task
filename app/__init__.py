from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = 't1NP63m4wnBg6nyHYKfmc2TpCOGI4nss'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///caycom.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'False'
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)
jwt = JWTManager(app)

from app import model, schema, resource, error_handler

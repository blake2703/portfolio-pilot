from flask import Flask
from flask_restx import Api
from .auth.views import auth_namespace
from .config.config import config_dict

def create_app(config=config_dict['dev']):
    app = Flask(__name__)
    
    
    app.config.from_object(obj=config)
    
    api = Api(app=app)
    
    api.add_namespace(ns=auth_namespace)
    
    return app
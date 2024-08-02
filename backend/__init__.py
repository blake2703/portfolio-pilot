from flask import Flask
from flask_restx import Api
from .auth.views import auth_namespace

def create_app():
    app = Flask(__name__)
    
    api = Api(app=app)
    
    api.add_namespace(ns=auth_namespace, path="/")
    
    return app
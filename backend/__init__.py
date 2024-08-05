from flask import Flask
from flask_restx import Api
from .auth.views import auth_namespace
from .stocks.views import stocks_namespace
from .config.config import config_dict
from .utils import db
from .models.users import User
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

def create_app(config=config_dict['dev']):
    app = Flask(__name__)
    
    
    app.config.from_object(obj=config)
    
    db.init_app(app=app)
    migrate = Migrate(app=app, db=db)
    
    jwt = JWTManager(app=app)
    
    api = Api(app=app)
    
    api.add_namespace(ns=auth_namespace)
    api.add_namespace(ns=stocks_namespace)
    
    
    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'User': User
        }
    
    return app
from flask import Flask
from flask_restx import Api
from .auth.views import auth_namespace
from .stocks.views import stocks_namespace
from .strategies.views import strategies_namespace
from .metrics.views import metrics_namespace
from .config.config import config_dict
from .utils import db
from .models.users import User
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager


def create_app(config=config_dict['dev']):
    app = Flask(__name__)
    
    # create app with the dev/prod/test config
    app.config.from_object(obj=config)
    
    # create db
    db.init_app(app=app)
    migrate = Migrate(app=app, db=db)
    
    jwt = JWTManager(app=app)
    
    # instantiate restx framework
    api = Api(app=app)
    
    # add namespaces to get access to routes/endpoints
    api.add_namespace(ns=auth_namespace)
    api.add_namespace(ns=stocks_namespace)
    api.add_namespace(ns=strategies_namespace)
    api.add_namespace(ns=metrics_namespace)
    
    
    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'User': User
        }
    
    return app
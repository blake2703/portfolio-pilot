import os
import sys
from flask import Flask

sys.path.append(os.getcwd())


def create_app():
    app = Flask(__name__)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    from .blueprints.index import bp as index_bp
    app.register_blueprint(index_bp)

    return app
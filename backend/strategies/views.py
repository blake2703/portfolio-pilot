from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from http import HTTPStatus
import json
import os

strategies_namespace = Namespace('strategies', description="Strategies namespace")


@strategies_namespace.route('/rsi2')
class Rsi2Endpoint(Resource):
    
    @jwt_required(refresh=True)
    def get(self):
        
        file_path = f"{os.getcwd()}/buys"
        
        if not os.path.exists(file_path):
            return {"message": "File not found"}, HTTPStatus.NOT_FOUND
        
        if os.path.getsize(file_path) == 0:
            return {"message": "No buys today"}, HTTPStatus.OK
        
        with open(f"{os.getcwd()}/buys") as file:
            data = json.load(file)
        
        return data, HTTPStatus.OK
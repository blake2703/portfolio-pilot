from flask_restx import Namespace, Resource, fields
from flask import request
from ..models.users import User
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus

auth_namespace = Namespace('auth', description="Authentication namespace")


signup_model = auth_namespace.model(
    'User',
    {
        'id': fields.Integer(),
        'first_name': fields.String(required=True, description="First name"),
        "last_name": fields.String(required=True, description="Last name"),
        'username': fields.String(required=True, description="A username"),
        'email': fields.String(required=True, description="Email"),
        'password': fields.String(required=True, description="A password")
    }
)

user_model = auth_namespace.model(
    'User',
    {
        'id': fields.Integer(),
        'first_name': fields.String(required=True, description="First name"),
        "last_name": fields.String(required=True, description="Last name"),
        'username': fields.String(required=True, description="A username"),
        'email': fields.String(required=True, description="Email"),
        'password': fields.String(required=True, description="A password"),
        'is_paid_member': fields.Boolean(description='User is a paid member')
    }
)

@auth_namespace.route('/signup')
class Signup(Resource):
    
    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(user_model)
    def post(self):
        data = request.get_json()
        
        new_user = User(
            first_name = data.get('first_name'),
            last_name = data.get('last_name'),
            username = data.get('username'),
            email = data.get('email'),
            password_hash = generate_password_hash(data.get('password'))
        )
        new_user.save()
        
        return new_user, HTTPStatus.CREATED
        


@auth_namespace.route('/login')
class Login(Resource):
    
    def post(self):
        pass
    
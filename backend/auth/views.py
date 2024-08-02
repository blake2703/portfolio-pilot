from flask_restx import Namespace, Resource, fields

auth_namespace = Namespace('auth', description="Authentication namespace")


@auth_namespace.route('/signup')
class Signup(Resource):
    
    def post(self):
        pass


@auth_namespace.route('/login')
class Login(Resource):
    
    def post(self):
        pass
    
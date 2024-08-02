from flask_restx import Namespace, Resource

auth_namespace = Namespace('auth', description="Authentication namespace")

@auth_namespace.route(urls="/")
class HelloAuth(Resource):
    
    def get(self):
        return {"message": "hello Auth"}
    
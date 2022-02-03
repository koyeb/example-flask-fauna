from flask import request
from flask_restx import Resource

from server.auth import parsers
from server.auth import repository
from server.auth import serializers
from server.api import api


ns = api.namespace('auth', description='Operations related to authorization')


@ns.route('/login')
class Login(Resource):

    @api.expect(parsers.login_args)
    @api.marshal_with(serializers.token)
    def post(self):
        """
        Exchange credentials to access token
        """
        credentials = parsers.login_args.parse_args(request)
        response = repository.login(
            credentials.get('email'), credentials.get('password'))
        return {"access_token": response.get("secret")}


@ns.route('/logout')
class Logout(Resource):

    @api.doc(security='apiKey')
    def post(self):
        """
        Logout user
        """
        repository.logout(request.headers.get("x-access-token"))
        return {'message': 'Logout successful'}


@ns.route('/signup')
class Signup(Resource):

    @api.expect(parsers.login_args)
    @api.marshal_with(serializers.token)
    def post(self):
        """
        Create user and exchange credentials to access token
        """
        credentials = parsers.login_args.parse_args(request)
        repository.signup(credentials.get('email'),
                          credentials.get('password'))
        response = repository.login(
            credentials.get('email'), credentials.get('password'))
        return {"access_token": response.get("secret")}


@ns.route('/users')
class Products(Resource):

    @api.doc(security='apiKey')
    def get(self):
        """
        Returns list of users.
        """
        return repository.get_users(request.headers.get("x-access-token"))

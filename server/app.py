from flask import Blueprint, Flask
from faunadb import errors as faunaErrors

from server.auth.controller import ns as auth_namespace
from server.api import api


@api.errorhandler(faunaErrors.BadRequest)
def fauna_error_handler(e):
    return {'message': e.errors[0].description}, 400


@api.errorhandler(faunaErrors.Unauthorized)
@api.errorhandler(faunaErrors.PermissionDenied)
def fauna_error_handler(e):
    return {'message': "Access forbidden"}, 403


app = Flask(__name__)
blueprint = Blueprint('api', __name__, url_prefix='/api')
api.init_app(blueprint)
api.add_namespace(auth_namespace)
app.register_blueprint(blueprint)


def main():
    app.run(debug=False)


if __name__ == "__main__":
    main()

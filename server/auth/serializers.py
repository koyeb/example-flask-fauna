from flask_restx import fields
from server.api import api


token = api.model('Tokens', {
    'access_token': fields.String(readOnly=True, description='Access token')
})

user = api.model('User', {
    'email': fields.String(attribute='data.email', required=True, description='User email'),
})

user_list = api.inherit('User list', {
    'data': fields.List(fields.Nested(user))
})

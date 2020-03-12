from flask_restplus import Namespace, fields


class UserDto:
    api = Namespace('users', description='user related operations')
    user = api.model('users', {
        'email': fields.String(required=True, description='user email address'),
        'name': fields.String(required=True, description='user name'),
        'surname': fields.String(required=True, description='user surname'),
        'password': fields.String(required=True, description='user password')

    })
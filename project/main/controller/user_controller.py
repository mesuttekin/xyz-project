from flask import request
from flask_restplus import Resource

from ..dto.user_dto import UserDto
from ..service.user_service import save_new_user, get_all_users, get_a_user, delete_user

api = UserDto.api
_user = UserDto.user


@api.route('/')
class UserList(Resource):
    @api.doc('list_of_registered_users')
    @api.marshal_list_with(_user, envelope='data')
    def get(self):
        """List all registered users"""
        return get_all_users()

    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    @api.expect(_user, validate=True)
    def post(self):
        """Creates a new User """
        data = request.json
        return save_new_user(data=data)


@api.route('/<email>')
@api.param('email', 'The User e-mail')
@api.response(404, 'User not found.')
class User(Resource):
    @api.doc('get a user')
    @api.marshal_with(_user)
    def get(self, email):
        """get a user given its e-mail"""
        user = get_a_user(email)
        if not user:
            api.abort(404)
        else:
            return user

    @api.doc('delete a user')
    def delete(self, email):
        """delete a user given its e-mail"""
        return delete_user(email)


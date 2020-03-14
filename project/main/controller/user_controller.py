from flask import request
from flask_restplus import Resource

from ..dto.user_dto import UserDto
from ..service.user_service import save_new_user, get_all_users, get_a_user, delete_user
from ..util.decorator import token_required

api = UserDto.api
_user = UserDto.user


@api.route('/')
class UserList(Resource):
    @api.doc('list_of_registered_users',
             params={'Authorization': {'in': 'header', 'description': 'JWT token'}}
             )
    @api.marshal_list_with(_user, envelope='data')
    @token_required
    def get(self, current_user_email):
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
    @api.doc('get a user',
             params={'Authorization': {'in': 'header', 'description': 'JWT token'}}
             )
    @api.marshal_with(_user)
    @token_required
    def get(self, email, current_user_email):
        """get a user given its e-mail"""
        user = get_a_user(email)
        if not user:
            api.abort(404)
        else:
            return user

    @api.doc('delete a user',
             params={'Authorization': {'in': 'header', 'description': 'JWT token'}}
             )
    @token_required
    def delete(self, email, current_user_email):
        """delete a user given its e-mail"""
        return delete_user(email)

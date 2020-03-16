from flask import request
from flask_restplus import Resource

from ..dto.project_dto import ProjectDto
from ..dto.user_dto import UserDto
from ..service.user_service import save_new_user, get_all_users, get_a_user, delete_user
from ..util.token_decorator import token_required

api = UserDto.api
_user = UserDto.user
_message = ProjectDto.message


@api.route('/')
class UserList(Resource):
    @api.doc('list_of_registered_users',
             params={'Authorization': {'in': 'header', 'description': 'JWT token'}}
             )
    @api.response(code=200, model=[_user], description='Success')
    @api.response(code=401, model=_message, description='Unauthorized')
    @token_required
    @api.marshal_list_with(_user, envelope='data')
    def get(self, current_user_email):
        """List all registered users"""
        return get_all_users()

    @api.response(code=201, model=_message, description='Created')
    @api.response(code=401, model=_message, description='Wrong Credential')
    @api.response(code=409, model=_message, description='Already exists')
    @api.doc('create a new user')
    @api.expect(_user, validate=True)
    def post(self):
        """Creates a new user """
        data = request.json
        return save_new_user(data=data)


@api.route('/<email>')
@api.param('email', 'The User e-mail')
@api.response(404, 'User not found.')
@api.response(code=401, model=_message, description='Unauthorized')
class User(Resource):
    @api.doc('get a user',
             params={'Authorization': {'in': 'header', 'description': 'JWT token'}}
             )
    @api.response(code=200, model=_user, description='Success')
    @token_required
    @api.marshal_with(_user)
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
    @api.response(code=200, model=_message, description='Success')
    @token_required
    def delete(self, email, current_user_email):
        """delete a user given its e-mail"""
        return delete_user(email)

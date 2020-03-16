from flask import request
from flask_restplus import Resource

from project.main.service.auth_service import Auth
from ..dto.auth_dto import AuthDto
from ..dto.project_dto import ProjectDto

api = AuthDto.api
user_auth = AuthDto.user_auth
_message = ProjectDto.message


@api.route('/login')
class UserLogin(Resource):
    """
        User Login Resource
    """

    @api.doc('user login')
    @api.response(code=200, model=user_auth, description='Success')
    @api.response(code=401, model=_message, description='Unauthorized')
    @api.expect(user_auth, validate=True)
    def post(self):
        # get the post data
        post_data = request.json
        return Auth.login_user(data=post_data)


@api.route('/logout')
class LogoutAPI(Resource):
    """
    Logout Resource
    """

    @api.doc('logout a user',
             params={'Authorization': {'in': 'header', 'description': 'JWT token'}})
    @api.response(code=200, model=_message, description='Success')
    @api.response(code=401, model=_message, description='Unauthorized')
    @api.response(code=403, model=_message, description='Forbidden')
    def post(self):
        # get auth token
        auth_header = request.headers.get('Authorization')
        return Auth.logout_user(auth_token=auth_header)

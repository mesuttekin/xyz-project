from flask import request
from flask_restplus import Resource

from .project_controller import api
from ..dto.project_dto import ProjectDto
from ..dto.project_user_dto import ProjectUserDto
from ..service.project_user_service import save_new_project_user, get_project_user, \
    delete_project_user, get_project_users
from ..util.token_decorator import project_owner_token_required

api_user = ProjectUserDto.api
_project_user = ProjectUserDto.project_user
_message = ProjectDto.message


@api.route('/<project_id>/users')
@api.param('project_id', 'The Project Id')
@api.response(404, 'Project not found.')
@api.response(code=401, model=_message, description='Unauthorized')
class ProjectUserList(Resource):

    @api.doc('list_of_added_project_user',
             params={'Authorization': {'in': 'header', 'description': 'JWT token'}}
             )
    @api.response(code=200, model=[_project_user], description='Success')
    @project_owner_token_required
    @api.marshal_list_with(_project_user, envelope='data')
    def get(self, project_id):
        """List all project user"""
        return get_project_users(project_id)

    @api.response(code=201, model=_message, description='Created')
    @api.response(code=409, model=_message, description='Already exists')
    @api.doc('Add a user to a project',
             params={'Authorization': {'in': 'header', 'description': 'JWT token'}}
             )
    @api.expect(_project_user, validate=True)
    @project_owner_token_required
    def post(self, project_id):
        """Add a user to a project """
        data = request.json
        return save_new_project_user(data=data, project_id=project_id)


@api.route('/<project_id>/users/<user_email>')
@api.param('project_id', 'The Project Id')
@api.response(404, 'User not found.')
@api.response(code=401, model=_message, description='Unauthorized')
class ProjectUser(Resource):

    @api.doc('get a project user',
             params={'Authorization': {'in': 'header', 'description': 'JWT token'}}
             )
    @api.response(code=200, model=_project_user, description='Success')
    @project_owner_token_required
    @api.marshal_with(_project_user)
    def get(self, project_id, user_email):
        """get a project user given its id"""
        project_user = get_project_user(project_id, user_email)
        if not project_user:
            api.abort(404)
        else:
            return project_user

    @api.doc('delete a project user',
             params={'Authorization': {'in': 'header', 'description': 'JWT token'}}
             )
    @api.response(code=200, model=_message, description='Success')
    @project_owner_token_required
    def delete(self, project_id, user_email):
        """delete a project user given its id"""
        return delete_project_user(project_id, user_email)

from flask import request
from flask_restplus import Resource

from ..dto.project_dto import ProjectDto
from ..service.project_service import get_user_projects, save_new_project, get_project, delete_project
from ..util.decorator import token_required, project_member_token_required, project_owner_token_required

api = ProjectDto.api
_project = ProjectDto.user


@api.route('/')
class ProjectList(Resource):

    @api.doc('list_of_added_project',
             params={'Authorization': {'in': 'header', 'description': 'JWT token'}}
             )
    @api.marshal_list_with(_project, envelope='data')
    @token_required
    def get(self, current_user_email):
        """List all user's project"""
        return get_user_projects(current_user_email)


    @api.response(201, 'Project successfully created.')
    @api.doc('create a new project')
    @api.expect(_project, validate=True)
    @token_required
    def post(self, current_user_email):
        """Creates a new Project """
        data = request.json
        return save_new_project(data=data, current_user_email=current_user_email)


@api.route('/<project_id>')
@api.param('project_id', 'The Project Id')
@api.response(404, 'Project not found.')
class Project(Resource):

    @api.doc('get a project',
             params={'Authorization': {'in': 'header', 'description': 'JWT token'}}
             )
    @api.marshal_with(_project)
    @project_member_token_required
    def get(self, project_id):
        """get a project given its id"""
        project = get_project(project_id)
        if not project:
            api.abort(404)
        else:
            return project


    @api.doc('delete a project',
             params={'Authorization': {'in': 'header', 'description': 'JWT token'}}
             )
    @project_owner_token_required
    def delete(self, project_id):
        """delete a project given its id"""
        return delete_project(project_id)



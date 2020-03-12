from flask import request
from flask_restplus import Resource

from ..dto.project_dto import ProjectDto
from ..dto.user_dto import UserDto
from ..service.project_service import get_user_projects, save_new_project, get_project, delete_project
from ..util.decorator import token_required

api = ProjectDto.api
_project = ProjectDto.user


@api.route('/')
class ProjectList(Resource):
    @api.doc('list_of_added_project',
             params={'project_id': 'Project Id',
                     'Authorization': {'in': 'header', 'description': 'JWT token'}}
             )
    @api.marshal_list_with(_project, envelope='data')
    def get(self):
        """List all user's project"""
        project_id = request.args.get('project_id')
        return get_user_projects(project_id)

    @api.response(201, 'Project successfully created.')
    @api.doc('create a new project')
    @api.expect(_project, validate=True)
    def post(self):
        """Creates a new Project """
        data = request.json
        return save_new_project(data=data)


@api.route('/<project_id>')
@api.param('project_id', 'The Project Id')
@api.response(404, 'Project not found.')
class Project(Resource):
    @api.doc('get a project',
             params={'Authorization': {'in': 'header', 'description': 'JWT token'}}
             )
    @api.marshal_with(_project)
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
    def delete(self, project_id):
        """delete a user given its e-mail"""
        return delete_project(project_id)

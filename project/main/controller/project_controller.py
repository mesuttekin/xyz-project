from flask import request
from flask_restplus import Resource

from ..dto.project_dto import ProjectDto
from ..dto.project_user_dto import ProjectUserDto
from ..service.project_service import get_user_projects, save_new_project, get_project, delete_project
from ..service.project_user_service import save_new_project_user, get_project_user, \
    delete_project_user, get_project_users

api = ProjectDto.api
_project = ProjectDto.user

api_user = ProjectUserDto.api
_project_user = ProjectUserDto.user


@api.route('/')
class ProjectList(Resource):
    @api.doc('list_of_added_project',
             params={'user_id': 'User Id',
                     'Authorization': {'in': 'header', 'description': 'JWT token'}}
             )
    @api.marshal_list_with(_project, envelope='data')
    def get(self):
        """List all user's project"""
        user_id = request.args.get('user_id')
        return get_user_projects(user_id)

    @api.response(201, 'Project successfully created.')
    @api.doc('create a new project')
    @api.expect(_project, validate=True)
    def post(self):
        """Creates a new Project """
        data = request.json
        # TODO:get user_email from token
        return save_new_project(data=data, user_email='ali@ali.com')


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
        """delete a project given its id"""
        return delete_project(project_id)


@api.route('/<project_id>/users')
@api.param('project_id', 'The Project Id')
@api.response(404, 'Project not found.')
class ProjectUserList(Resource):
    @api.doc('list_of_added_project_user',
             params={'Authorization': {'in': 'header', 'description': 'JWT token'}}
             )
    @api.marshal_list_with(_project_user, envelope='data')
    def get(self, project_id):
        """List all project user"""
        return get_project_users(project_id)

    @api.response(201, 'Project User successfully created.')
    @api.doc('create a new project user')
    @api.expect(_project_user, validate=True)
    def post(self, project_id):
        """Creates a new Project User """
        data = request.json
        return save_new_project_user(data=data)


@api.route('/<project_id>/users/<user_email>')
@api.param('project_id', 'The Project Id')
@api.response(404, 'User not found.')
class ProjectUser(Resource):
    @api.doc('get a project user',
             params={'Authorization': {'in': 'header', 'description': 'JWT token'}}
             )
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
    def delete(self, project_id, user_email):
        """delete a project user given its id"""
        return delete_project_user(project_id, user_email)
from flask_restplus import Namespace, fields


class ProjectUserDto:
    api = Namespace('project_user', description='project-user related operations')
    user = api.model('project_user', {
        'project_id': fields.Integer(required=True, description='project id'),
        'user_id': fields.Integer(required=True, description='user id'),
        'project_owner': fields.Boolean(required=True, description='project owner')

    })
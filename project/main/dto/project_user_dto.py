from flask_restplus import Namespace, fields


class ProjectUserDto:
    api = Namespace('project_user', description='project-user related operations')
    user = api.model('project_user', {
        'project_id': fields.Integer(required=True, description='project id'),
        'user_email': fields.String(required=True, description='user email'),
        'project_owner': fields.Boolean(required=True, description='project owner')

    })

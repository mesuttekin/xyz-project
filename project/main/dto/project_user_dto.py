from flask_restplus import Namespace, fields


class ProjectUserDto:
    api = Namespace('project_user', description='project-user related operations')
    project_user = api.model('project_user', {
        'user_email': fields.String(required=True, description='user email'),
        'project_owner': fields.Boolean(required=True, description='project owner')

    })

from flask_restplus import Namespace, fields


class ProjectDto:
    api = Namespace('projects', description='project related operations')
    user = api.model('projects', {
        'name': fields.String(required=True, description='user name')
    })

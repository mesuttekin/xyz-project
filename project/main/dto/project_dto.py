from flask_restplus import Namespace, fields


class ProjectDto:
    api = Namespace('projects', description='project related operations')
    project = api.model('projects', {
        'name': fields.String(required=True, description='project name')
    })

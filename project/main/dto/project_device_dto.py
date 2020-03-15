from flask_restplus import Namespace, fields


class ProjectDeviceDto:
    api = Namespace('project_device', description='project device related operations')
    project_device = api.model('project_device', {
        'device_id': fields.Integer(required=True, description='device id')
    })

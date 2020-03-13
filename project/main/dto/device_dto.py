from flask_restplus import Namespace, fields


class DeviceDto:
    api = Namespace('devices', description='device related operations')
    user = api.model('devices', {
        'name': fields.String(required=True, description='device name'),
        'serial_number': fields.String(required=True, description='device serial number'),
        'project_id': fields.Integer(required=True, description='device project id')
    })

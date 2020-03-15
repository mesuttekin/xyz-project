from flask_restplus import Namespace, fields


class DeviceDto:
    api = Namespace('devices', description='device related operations')
    device = api.model('devices', {
        'name': fields.String(required=True, description='device name'),
        'serial_number': fields.String(required=True, description='device serial number', pattern="^[0-9]{5}$")
    })

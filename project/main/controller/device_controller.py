from flask import request
from flask_restplus import Resource

from ..dto.device_dto import DeviceDto
from ..service.device_service import get_project_devices, save_new_device, get_device, delete_device

api = DeviceDto.api
_device = DeviceDto.user


@api.route('/')
class DeviceList(Resource):
    @api.doc('list_of_added_device',
             params={'project_id': 'Project Id',
                     'Authorization': {'in': 'header', 'description': 'JWT token'}}
             )
    @api.marshal_list_with(_device, envelope='data')
    def get(self):
        """List all project devices"""
        project_id = request.args.get('project_id')
        return get_project_devices(project_id)

    @api.response(201, 'Device successfully created.')
    @api.doc('create a new device')
    @api.expect(_device, validate=True)
    def post(self):
        """Creates a new Device """
        data = request.json
        return save_new_device(data=data)


@api.route('/<device_id>')
@api.param('device_id', 'The Device Id')
@api.response(404, 'Device not found.')
class Device(Resource):
    @api.doc('get a device',
             params={'Authorization': {'in': 'header', 'description': 'JWT token'}}
             )
    @api.marshal_with(_device)
    def get(self, device_id):
        """get a device given its id"""
        device = get_device(device_id)
        if not device:
            api.abort(404)
        else:
            return device

    @api.doc('delete a device',
             params={'Authorization': {'in': 'header', 'description': 'JWT token'}}
             )
    def delete(self, device_id):
        """delete a device given its id"""
        return delete_device(device_id)

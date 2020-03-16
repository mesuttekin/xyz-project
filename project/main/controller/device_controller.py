from flask import request
from flask_restplus import Resource

from ..dto.device_dto import DeviceDto
from ..service.device_service import get_devices, save_new_device, get_device, delete_device
from ..util.decorator import token_required

api = DeviceDto.api
_device = DeviceDto.device


@api.route('/')
class DeviceList(Resource):

    @api.doc('list_of_devices',
             params={'Authorization': {'in': 'header', 'description': 'JWT token'}}
             )
    @api.marshal_list_with(_device, envelope='data')
    @token_required
    def get(self, current_user_email):
        """List all devices"""
        return get_devices(current_user_email)

    @api.response(201, 'Device successfully created.')
    @api.doc('create a new device',
             params={'Authorization': {'in': 'header', 'description': 'JWT token'}}
             )
    @api.expect(_device, validate=True)
    @token_required
    def post(self, current_user_email):
        """Creates a new device """
        data = request.json
        return save_new_device(data=data, current_user_email=current_user_email)


@api.route('/<device_id>')
@api.param('device_id', 'The Device Id')
@api.response(404, 'Device not found.')
class Device(Resource):

    @api.doc('get a device',
             params={'Authorization': {'in': 'header', 'description': 'JWT token'}}
             )
    @api.marshal_with(_device)
    @token_required
    def get(self, device_id, current_user_email):
        """get a device given its id"""
        device = get_device(device_id)
        if not device:
            api.abort(404)
        else:
            return device

    @api.doc('delete a device',
             params={'Authorization': {'in': 'header', 'description': 'JWT token'}}
             )
    @token_required
    def delete(self, device_id, current_user_email):
        """delete a device given its id"""
        return delete_device(device_id)

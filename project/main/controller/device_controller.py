from flask import request
from flask_restplus import Resource

from ..dto.device_dto import DeviceDto
from ..dto.project_dto import ProjectDto
from ..service.device_service import get_devices, save_new_device, get_device, delete_device
from ..util.token_decorator import token_required

api = DeviceDto.api
_device = DeviceDto.device
_message = ProjectDto.message


@api.route('/')
@api.response(code=401, model=_message, description='Unauthorized')
class DeviceList(Resource):

    @api.doc('list_of_devices',
             params={'Authorization': {'in': 'header', 'description': 'JWT token'}}
             )
    @api.response(code=200, model=_device, description='Success')
    @token_required
    @api.marshal_list_with(_device, envelope='data')
    def get(self, current_user_email):
        """List all devices"""
        return get_devices(current_user_email)

    @api.response(code=201, model=_message, description='Created')
    @api.response(code=409, model=_message, description='Already exists')
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
@api.response(code=401, model=_message, description='Unauthorized')
class Device(Resource):

    @api.doc('get a device',
             params={'Authorization': {'in': 'header', 'description': 'JWT token'}}
             )
    @api.response(code=200, model=_device, description='Success')
    @token_required
    @api.marshal_with(_device)
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
    @api.response(code=200, model=_message, description='Success')
    @token_required
    def delete(self, device_id, current_user_email):
        """delete a device given its id"""
        return delete_device(device_id)

from flask import request
from flask_restplus import Resource

from .project_controller import api
from ..dto.device_dto import DeviceDto
from ..service.device_service import get_project_devices, save_new_device, get_device, delete_device
from ..util.decorator import project_member_token_required

api_device = DeviceDto.api
_device = DeviceDto.user


@api.route('/<project_id>/devices')
@api.param('project_id', 'The Project Id')
class DeviceList(Resource):
    @api.doc('list_of_added_device',
             params={'Authorization': {'in': 'header', 'description': 'JWT token'}}
             )
    @api.marshal_list_with(_device, envelope='data')
    @project_member_token_required
    def get(self, project_id):
        """List all project devices"""
        return get_project_devices(project_id)


    @api.response(201, 'Device successfully created.')
    @api.doc('create a new device')
    @api.expect(_device, validate=True)
    @project_member_token_required
    def post(self, project_id):
        """Creates a new Device """
        device = request.json
        return save_new_device(data=device)


@api.route('/<project_id>/devices/<device_id>')
@api.param('device_id', 'The Device Id')
@api.response(404, 'Device not found.')
@api.param('project_id', 'The Project Id')
class Device(Resource):
    @api.doc('get a device',
             params={'Authorization': {'in': 'header', 'description': 'JWT token'}}
             )
    @api.marshal_with(_device)
    @project_member_token_required
    def get(self, project_id, device_id):
        """get a device given its id"""
        device = get_device(device_id)
        if not device:
            api.abort(404)
        else:
            return device


    @api.doc('delete a device',
             params={'Authorization': {'in': 'header', 'description': 'JWT token'}}
             )
    @project_member_token_required
    def delete(self, project_id, device_id):
        """delete a device given its id"""
        return delete_device(device_id)

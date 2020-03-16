from flask import request
from flask_restplus import Resource

from .project_controller import api
from ..dto.project_device_dto import ProjectDeviceDto
from ..dto.project_dto import ProjectDto
from ..service.project_device_service import get_project_devices, save_new_project_device, get_project_device, \
    delete_project_device
from ..util.token_decorator import project_member_token_required

api_device_project = ProjectDeviceDto.api
_project_device = ProjectDeviceDto.project_device
_message = ProjectDto.message


@api.route('/<project_id>/devices')
@api.param('project_id', 'The Project Id')
@api.response(code=401, model=_message, description='Unauthorized')
class ProjectDeviceList(Resource):
    @api.doc('list_of_added_project_device',
             params={'Authorization': {'in': 'header', 'description': 'JWT token'}}
             )
    @api.response(code=200, model=[_project_device], description='Success')
    @project_member_token_required
    @api.marshal_list_with(_project_device, envelope='data')
    def get(self, project_id):
        """List all project devices"""
        return get_project_devices(project_id)

    @api.response(code=201, model=_message, description='Created')
    @api.response(code=409, model=_message, description='Already exists')
    @api.doc('Add a new device to a project',
             params={'Authorization': {'in': 'header', 'description': 'JWT token'}}
             )
    @api.expect(_project_device, validate=True)
    @project_member_token_required
    def post(self, project_id):
        """Add a new device to a project """
        device = request.json
        return save_new_project_device(project_device=device, project_id=project_id)


@api.route('/<project_id>/devices/<device_id>')
@api.param('device_id', 'The Device Id')
@api.response(404, 'Project device not found.')
@api.response(code=401, model=_message, description='Unauthorized')
@api.param('project_id', 'The Project Id')
class ProjectDevice(Resource):
    @api.doc('get a project device',
             params={'Authorization': {'in': 'header', 'description': 'JWT token'}}
             )
    @api.response(code=200, model=_project_device, description='Success')
    @project_member_token_required
    @api.marshal_with(_project_device)
    def get(self, project_id, device_id):
        """get a project device given its id"""
        device = get_project_device(project_id, device_id)
        if not device:
            api.abort(404)
        else:
            return device

    @api.doc('delete a project device',
             params={'Authorization': {'in': 'header', 'description': 'JWT token'}}
             )
    @api.response(code=200, model=_message, description='Success')
    @project_member_token_required
    def delete(self, project_id, device_id):
        """delete a project device given its id"""
        return delete_project_device(device_id)

import datetime

from project.main import db

from project.main.model.project_device import ProjectDevice


def save_new_project_device(project_device, project_id):
    _project_device = ProjectDevice.query.filter_by(device_id=project_device['device_id'], project_id=project_id).first()
    if not _project_device:
        new_device = ProjectDevice(
            device_id=project_device['device_id'],
            project_id=project_id,
            created_date=datetime.datetime.utcnow()
        )
        save_changes(new_device)
        response_object = {
            'status': 'success',
            'message': 'Successfully added.',
            'device_id': new_device.id
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Device id has already assigned to the project.',
        }
        return response_object, 409


def get_project_devices(project_id):
    # TODO: filter with user_id
    return ProjectDevice.query.filter_by(project_id=project_id).all()


def get_project_device(project_id, device_id):
    return ProjectDevice.query.filter_by(project_id=project_id, device_id=device_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.flush()
    db.session.commit()


def delete_project_device(project_device_id):
    project_device = ProjectDevice.query.filter_by(id=project_device_id).first()
    if project_device:
        delete_device_from_db(project_device)
        response_object = {
            'status': 'success',
            'message': 'Successfully deleted.'
        }
        return response_object, 200
    else:
        response_object = {
            'status': 'fail',
            'message': "No device found!",
        }
        return response_object, 404


def delete_device_from_db(device):
    db.session.delete(device)
    db.session.commit()

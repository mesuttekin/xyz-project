import datetime

from project.main import db
from project.main.model.device import Device


def save_new_device(data, current_user_email):
    device = Device.query.filter_by(serial_number=data['serial_number']).first()
    if not device:
        new_device = Device(
            name=data['name'],
            serial_number=data['serial_number'],
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
            'message': 'Device serial number already exists. Please change the serial number.',
        }
        return response_object, 409


def get_devices(current_user_email):
    return Device.query.all()


def get_device(device_id):
    return Device.query.filter_by(id=device_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.flush()
    db.session.commit()


def delete_device(device_id):
    device = Device.query.filter_by(id=device_id).first()
    if device:
        delete_device_from_db(device)
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

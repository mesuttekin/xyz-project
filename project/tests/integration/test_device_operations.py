import datetime
import json

from project.tests.integration.base import BaseTestCase
from project.tests.integration.operation_helper import add_project

project_id = 0
def add_device(self):
    response = add_project(self, self.authorization)
    data = json.loads(response.data.decode())
    global project_id
    project_id = data['project_id']
    return self.client.post(
        '/projects/' + str(project_id) + '/devices',
        data=json.dumps(dict(
            name='test device name',
            serial_number='12345',
            project_id=data['project_id']
        )),
        headers={'Authorization': self.authorization},
        content_type='application/json'
    )

def add_second_device(self):
    return self.client.post(
        '/projects/' + str(project_id) + '/devices',
        data=json.dumps(dict(
            name='test device name',
            serial_number='12345',
            project_id=project_id
        )),
        headers={'Authorization': self.authorization},
        content_type='application/json'
    )

def add_device_with_invalid_project_id(self):

    return self.client.post(
        '/projects/' + str(project_id) + '/devices',
        data=json.dumps(dict(
            name='test device name',
            serial_number='12345',
            project_id=0
        )),
        headers={'Authorization': self.authorization},
        content_type='application/json'
    )

def delete_device(self, device_id):
    return self.client.delete(
        '/projects/' + str(project_id) + '/devices/' + str(device_id),
        headers={'Authorization': self.authorization},
        content_type='application/json'
    )

def get_device(self, device_id):
    return self.client.get(
        '/projects/' + str(project_id) + '/devices/' + str(device_id),
        headers={'Authorization': self.authorization},
        content_type='application/json'
    )

def get_devices(self):
    return self.client.get(
        '/projects/' + str(project_id) + '/devices',
        headers={'Authorization': self.authorization},
        content_type='application/json'
    )


class TestUserController(BaseTestCase):

    def test_givenDeviceData_whenCallPost_thenAddTheDevice(self):
        """ Test for add device """
        with self.client:
            response = add_device(self)
            data = json.loads(response.data.decode())
            self.assertEqual('success', data['status'])
            self.assertEqual('Successfully added.', data['message'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(201, response.status_code)

    def test_givenDeviceDataInvalidProjectId_whenCallPost_thenReturn401(self):
        """ Test for add device with invalid project Id """
        with self.client:
            response = add_device_with_invalid_project_id(self)
            data = json.loads(response.data.decode())
            self.assertEqual('fail', data['status'])
            self.assertEqual('Provide a valid project member auth token.', data['message'] )
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(401, response.status_code)

    def test_givenNonProjectMemberUser_whenCallPost_thenReturn401(self):
        """ Test for add device with non member user """
        with self.client:
            response = add_device_with_invalid_project_id(self)
            data = json.loads(response.data.decode())
            self.assertEqual('fail', data['status'])
            self.assertEqual('Provide a valid project member auth token.', data['message'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(401, response.status_code)

    def test_givenDeviceId_whenCallGet_thenGetTheDevice(self):
        """ Get a device"""
        response = add_device(self)
        data = json.loads(response.data.decode())
        with self.client:
            response = get_device(self, data['device_id'])
            data = json.loads(response.data.decode())
            self.assertEqual('test device name', data['name'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(200, response.status_code)

    def test_givenNA_whenCallGet_thenGetAllDevice(self):
        """ List all devices"""
        response = add_device(self)
        data = json.loads(response.data.decode())
        with self.client:
            response = get_devices(self)
            data = json.loads(response.data.decode())['data']
            self.assertEqual(1, len(data))
            self.assertEqual('test device name', data[0]['name'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(200, response.status_code)

    def test_givenAlreadyAddedDevice_whenCallPost_thenShouldReturn409(self):
        """ Test add device with already added serial number"""
        add_device(self)
        with self.client:
            response = add_second_device(self)
            data = json.loads(response.data.decode())
            self.assertEqual('fail', data['status'])
            self.assertEqual(
                'Device serial number already exists. Please change the serial number.',
                data['message'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(409, response.status_code)

    def test_givenAlreadyAddedDevice_whenCallDelete_thenDeleteSuccessfully(self):
        """ Test delete already added device"""
        response = add_device(self)
        data = json.loads(response.data.decode())
        with self.client:
            response = delete_device(self, data['device_id'])
            data = json.loads(response.data.decode())
            self.assertEqual('success', data['status'])
            self.assertEqual(
                'Successfully deleted.',
                data['message'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(200, response.status_code)

    def test_givenNonAddedDevice_whenCallDelete_thenShouldReturn404(self):
        """ Test delete non added device"""
        with self.client:
            response = delete_device(self, '324234235433453')
            data = json.loads(response.data.decode())
            self.assertEqual('fail', data['status'])
            self.assertEqual(
                'Provide a valid project member auth token.',
                data['message'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(401, response.status_code)
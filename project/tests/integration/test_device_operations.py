import json

from project.tests.integration.base import BaseTestCase
from project.tests.integration.operation_helper import add_device


def add_second_device(self):
    return self.client.post(
        '/devices',
        data=json.dumps(dict(
            name='test device name',
            serial_number='12345'
        )),
        headers={'Authorization': self.authorization},
        content_type='application/json'
    )


def add_device_with_invalid_device_id(self):
    return self.client.post(
        '/devices',
        data=json.dumps(dict(
            name='test device name',
            serial_number='12345',
            device_id=0
        )),
        headers={'Authorization': self.authorization},
        content_type='application/json'
    )


def delete_device(self, device_id):
    return self.client.delete(
        '/devices/' + str(device_id),
        headers={'Authorization': self.authorization},
        content_type='application/json'
    )


def get_device(self, device_id):
    return self.client.get(
        '/devices/' + str(device_id),
        headers={'Authorization': self.authorization},
        content_type='application/json'
    )


def get_devices(self):
    return self.client.get(
        '/devices/',
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

    def test_givenDeviceId_whenCallGet_thenGetTheDevice(self):
        """ Get a device"""
        response = add_device(self)
        data = json.loads(response.data.decode())
        with self.client:
            response = get_device(self, data['device_id'])
            data = json.loads(response.data.decode())
            self.assertTrue(data['name'] == 'test device name')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(200, response.status_code)

    def test_givenAuthorization_whenCallGet_thenGetAllUserDevice(self):
        """ List all user devices"""
        add_device(self)
        with self.client:
            response = get_devices(self)
            data = json.loads(response.data.decode())['data']
            self.assertEqual(1, len(data))
            self.assertEqual('test device name', data[0]['name'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(200, response.status_code)

    def test_givenUnauthorizedUser_whenCallGet_thenReturn401(self):
        """Test unauthorized user to not get a device"""
        add_device(self)
        with self.client:
            self.authorization = "fake_token"
            response = get_devices(self)
            self.assertEqual(401, response.status_code)

    def test_givenAlreadyAddedDevice_whenCallPost_thenShouldReturn409(self):
        """ Test add device with already added name"""
        add_device(self)
        with self.client:
            response = add_device(self)
            data = json.loads(response.data.decode())
            self.assertEqual('fail', data['status'])
            self.assertEqual('Device serial number already exists. Please change the serial number.',
                             data['message']
                             )
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(409, response.status_code)

    def test_givenAlreadyAddedDevice_whenCallDelete_thenDeleteSuccessfully(self):
        """ Test delete already added device"""
        response = add_device(self)
        data = json.loads(response.data.decode())
        with self.client:
            response = delete_device(self, data['device_id'])
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(
                data['message'] == 'Successfully deleted.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(200, response.status_code)

    def test_givenNonAddedDevice_whenCallDelete_thenShouldReturn404(self):
        """ Test delete non added device"""
        with self.client:
            response = delete_device(self, 'fake_device_id')
            data = json.loads(response.data.decode())
            self.assertEqual('fail', data['status'])
            self.assertEqual(
                'No device found!',
                data['message'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(404, response.status_code)

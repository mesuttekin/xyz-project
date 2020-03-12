
import json

from project.tests.integration.base import BaseTestCase


def register_user(self):
    return self.client.post(
        '/users/',
        data=json.dumps(dict(
            email='ali@gmail.com',
            name='name',
            surname='surname',
            password='12345'
        )),
        content_type='application/json'
    )

def delete_user(self):
    return self.client.delete(
        '/users/ali@gmail.com',
        content_type='application/json'
    )

def get_a_user(self):
    return self.client.get(
        '/users/ali@gmail.com',
        content_type='application/json'
    )

def get_users(self):
    return self.client.get(
        '/users/',
        content_type='application/json'
    )


class TestUserController(BaseTestCase):

    def test_givenUserEmail_whenCallGet_thenTheUser(self):
        """ Get a registered user"""
        register_user(self)
        with self.client:
            response = get_a_user(self)
            data = json.loads(response.data.decode())
            self.assertTrue(data['email'] == 'ali@gmail.com')
            self.assertTrue(data['name'] == 'name')
            self.assertTrue(data['surname'] == 'surname')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(200, response.status_code)

    def test_givenNA_whenCallGet_thenGetAllUser(self):
        """ List all registered users"""
        register_user(self)
        with self.client:
            response = get_users(self)
            data = json.loads(response.data.decode())['data']
            self.assertTrue(len(data) == 1)
            self.assertTrue(data[0]['email'] == 'ali@gmail.com')
            self.assertTrue(data[0]['name'] == 'name')
            self.assertTrue(data[0]['surname'] == 'surname')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(200, response.status_code)

    def test_givenUserData_whenCallPost_thenRegisterTheUser(self):
        """ Test for user registration """
        with self.client:
            response = register_user(self)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(201, response.status_code)

    def test_givenAlreadyRegisteredUser_whenCallPost_thenShouldReturn409(self):
        """ Test registration with already registered email"""
        register_user(self)
        with self.client:
            response = register_user(self)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'User already exists. Please Log in.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(409, response.status_code)

    def test_givenAlreadyRegisteredUser_whenCallDelete_thenDeleteSuccessfully(self):
        """ Test delete already registered user"""
        register_user(self)
        with self.client:
            response = delete_user(self)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(
                data['message'] == 'Successfully deleted.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(200, response.status_code)

    def test_givenNonRegisteredUser_whenCallDelete_thenShouldReturn404(self):
        """ Test delete non registered user"""
        with self.client:
            response = delete_user(self)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'No user found!')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(404, response.status_code)
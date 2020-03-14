import json

from project.tests.integration.base import BaseTestCase
from project.tests.integration.operation_helper import register_user, get_a_user, get_users, delete_user, \
    register_second_user


class TestUserController(BaseTestCase):

    def test_givenUserEmail_whenCallGet_thenGetTheUser(self):
        """ Get a registered user"""
        response = register_user(self)
        data = json.loads(response.data.decode())
        with self.client:
            response = get_a_user(self, data['Authorization'])
            data = json.loads(response.data.decode())
            self.assertTrue(data['email'] == 'ali@gmail.com')
            self.assertTrue(data['name'] == 'name')
            self.assertTrue(data['surname'] == 'surname')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(200, response.status_code)

    def test_givenNA_whenCallGet_thenGetAllUser(self):
        """ List all registered users"""
        response = register_user(self)
        data = json.loads(response.data.decode())
        with self.client:
            response = get_users(self, data['Authorization'])
            data = json.loads(response.data.decode())['data']
            self.assertEqual(2, len(data))
            self.assertEqual('ali@gmail.com', data[1]['email'])
            self.assertEqual('name', data[1]['name'])
            self.assertEqual('surname', data[1]['surname'])
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
        response = register_user(self)
        data = json.loads(response.data.decode())
        with self.client:
            response = delete_user(self, data['Authorization'])
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(
                data['message'] == 'Successfully deleted.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(200, response.status_code)

    def test_givenNonRegisteredUser_whenCallDelete_thenShouldReturn404(self):
        """ Test delete non registered user"""
        response = register_second_user(self)
        data = json.loads(response.data.decode())
        with self.client:
            response = delete_user(self, data['Authorization'])
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'No user found!')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(404, response.status_code)

    def test_givenInvalidToken_whenCallDelete_thenReturn401(self):
        """ Test invalid token with delete"""
        with self.client:
            response = delete_user(self, "wrong_token")
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'Invalid token. Please log in again.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(401, response.status_code)

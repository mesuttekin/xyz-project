import json

from project.tests.integration.base import BaseTestCase
from project.tests.integration.operation_helper import add_project, register_user

project_id = 0
current_user_email = 'auth@gmail.com'


def add_project_user(self):
    response = add_project(self, self.authorization)
    data = json.loads(response.data.decode())
    global project_id
    project_id = data['project_id']

    return self.client.post(
        '/projects/' + str(project_id) + '/users',
        data=json.dumps(dict(
            project_id=project_id,
            user_email='ali@gmail.com',
            project_owner=False
        )),
        headers={'Authorization': self.authorization},
        content_type='application/json'
    )


def add_non_project_owner_user(self):
    response = add_project(self, self.authorization)
    data = json.loads(response.data.decode())
    global project_id
    project_id = data['project_id']

    response = register_user(self)
    current_user = json.loads(response.data.decode())

    return self.client.post(
        '/projects/' + str(project_id) + '/users',
        data=json.dumps(dict(
            project_id=project_id,
            user_email='ali@gmail.com',
            project_owner=False
        )),
        headers={'Authorization': current_user['Authorization']},
        content_type='application/json'
    )


def add_second_project_user(self):
    return self.client.post(
        '/projects/' + str(project_id) + '/users',
        data=json.dumps(dict(
            project_id=project_id,
            user_email=current_user_email,
            project_owner=False
        )),
        headers={'Authorization': self.authorization},
        content_type='application/json'
    )


def delete_project_user(self, _user_email=current_user_email):
    return self.client.delete(
        '/projects/' + str(project_id) + '/users/' + str(_user_email),
        content_type='application/json',
        headers={'Authorization': self.authorization},
    )


def get_project_user(self):
    return self.client.get(
        '/projects/' + str(project_id) + '/users/' + str(current_user_email),
        content_type='application/json',
        headers={'Authorization': self.authorization},
    )


def get_project_users(self):
    return self.client.get(
        '/projects/' + str(project_id) + '/users',
        content_type='application/json',
        headers={'Authorization': self.authorization},

    )


class TestUserController(BaseTestCase):

    def test_givenProjectUserData_whenCallPost_thenAddTheProjectUser(self):
        """ Test for add project user """
        with self.client:
            response = add_project_user(self)
            data = json.loads(response.data.decode())
            self.assertEqual('success', data['status'])
            self.assertEqual('Successfully added.', data['message'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(201, response.status_code)

    def test_givenUserEmailProjectId_whenCallGet_thenGetTheProjectUser(self):
        """ Get a project """
        add_project_user(self)
        with self.client:
            response = get_project_user(self)
            data = json.loads(response.data.decode())
            self.assertEqual(project_id, data['project_id'])
            self.assertEqual(current_user_email, data['user_email'])
            self.assertTrue(data['project_owner'] is True)
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(200, response.status_code)

    def test_givenNA_whenCallGet_thenGetAllProject(self):
        """ List all projects"""
        add_project_user(self)
        with self.client:
            response = get_project_users(self)
            data = json.loads(response.data.decode())['data']
            self.assertEqual(2, len(data))
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(200, response.status_code)

    def test_givenAlreadyAddedProject_whenCallPost_thenShouldReturn409(self):
        """ Test add project with already added name"""
        add_project_user(self)
        with self.client:
            response = add_second_project_user(self)
            data = json.loads(response.data.decode())
            self.assertEqual('fail', data['status'])
            self.assertEqual(
                'Same user has already assigned to the project.', data['message'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(409, response.status_code)

    def test_givenAlreadyAddedProject_whenCallDelete_thenDeleteSuccessfully(self):
        """ Test delete already added project"""
        add_project_user(self)
        with self.client:
            response = delete_project_user(self)
            data = json.loads(response.data.decode())
            self.assertEqual('success', data['status'])
            self.assertEqual('Successfully deleted.', data['message'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(200, response.status_code)

    def test_givenNonAddedProjectUser_whenCallDelete_thenShouldReturn404(self):
        """ Test delete non added project user"""
        add_project_user(self)
        with self.client:
            response = delete_project_user(self, 'fake_user_email')
            data = json.loads(response.data.decode())
            self.assertEqual('fail', data['status'])
            self.assertEqual('No project user found!', data['message'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(404, response.status_code)

    def test_givenNonProjectOwnerUser_whenCallPost_thenShouldReturn401(self):
        """ Test delete with non project owner user"""

        with self.client:
            response = add_non_project_owner_user(self)
            data = json.loads(response.data.decode())
            self.assertEqual('fail', data['status'])
            self.assertEqual('Provide a valid project owner auth token.', data['message'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(401, response.status_code)

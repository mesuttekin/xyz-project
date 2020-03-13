import datetime
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


def add_project(self):
    return self.client.post(
        '/projects/',
        data=json.dumps(dict(
            name='test project name'
        )),
        content_type='application/json'
    )


project_id = 0
user_email = ''

def add_project_user(self):
    response = add_project(self)
    data = json.loads(response.data.decode())
    global project_id
    project_id = data['project_id']

    response = register_user(self)
    data = json.loads(response.data.decode())
    global user_email
    user_email = data['user_email']

    return self.client.post(
        '/projects/' + str(project_id) + '/users',
        data=json.dumps(dict(
            project_id=project_id,
            user_email='ali@gmail.com',
            project_owner=False
        )),
        content_type='application/json'
    )

def add_second_project_user(self):
    return self.client.post(
        '/projects/' + str(project_id) + '/users',
        data=json.dumps(dict(
            project_id=project_id,
            user_email=user_email,
            project_owner=False
        )),
        content_type='application/json'
    )


def delete_project_user(self):
    return self.client.delete(
        '/projects/' + str(project_id) + '/users/' + str(user_email),
        content_type='application/json'
    )


def get_project_user(self):
    return self.client.get(
        '/projects/' + str(project_id) + '/users/' + str(user_email),
        content_type='application/json'
    )


def get_project_users(self):
    return self.client.get(
        '/projects/' + str(project_id) + '/users',
        content_type='application/json'
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

    def test_givenProjectId_whenCallGet_thenGetTheProject(self):
        """ Get a project """
        add_project_user(self)
        with self.client:
            response = get_project_user(self)
            data = json.loads(response.data.decode())
            self.assertEqual(project_id, data['project_id'])
            self.assertEqual(user_email, data['user_email'])
            self.assertTrue(data['project_owner']  is False)
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(200, response.status_code)

    def test_givenNA_whenCallGet_thenGetAllProject(self):
        """ List all projects"""
        add_project_user(self)
        with self.client:
            response = get_project_users(self)
            data = json.loads(response.data.decode())['data']
            self.assertEqual(2, len(data))
            self.assertEqual(project_id, data[1]['project_id'])
            self.assertEqual(user_email, data[1]['user_email'])
            self.assertTrue(data[1]['project_owner'] is False)
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

    def test_givenNonAddedProject_whenCallDelete_thenShouldReturn404(self):
        """ Test delete non added project"""
        with self.client:
            response = delete_project_user(self)
            data = json.loads(response.data.decode())
            self.assertEqual('fail', data['status'])
            self.assertEqual('No project user found!', data['message'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(404, response.status_code)

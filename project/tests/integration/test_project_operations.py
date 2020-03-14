
import json

from project.main.service.user_service import generate_token
from project.tests.integration.base import BaseTestCase
from project.tests.integration.operation_helper import add_project, get_project, get_projects, delete_project, \
    register_user





class TestUserController(BaseTestCase):


    def test_givenProjectData_whenCallPost_thenAddTheProject(self):
        """ Test for add project """
        with self.client:
            response = add_project(self, self.authorization)
            data = json.loads(response.data.decode())
            self.assertEqual('success', data['status'])
            self.assertEqual('Successfully added.', data['message'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(201, response.status_code)

    def test_givenProjectId_whenCallGet_thenGetTheProject(self):
        """ Get a project"""
        response = add_project(self, self.authorization)
        data = json.loads(response.data.decode())
        with self.client:
            response = get_project(self, data['project_id'], self.authorization)
            data = json.loads(response.data.decode())
            self.assertTrue(data['name'] == 'test project name')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(200, response.status_code)

    def test_givenAuthorization_whenCallGet_thenGetAllUserProject(self):
        """ List all user projects"""
        add_project(self, self.authorization)
        with self.client:
            response = get_projects(self, self.authorization)
            data = json.loads(response.data.decode())['data']
            self.assertEqual(1, len(data))
            self.assertEqual('test project name', data[0]['name'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(200, response.status_code)

    def test_givenUnauthorizedUser_whenCallGet_thenReturn401(self):
        """ List all projects"""
        add_project(self, self.authorization)
        with self.client:
            response = get_projects(self, "fake_token")
            self.assertEqual(401, response.status_code)

    def test_givenAlreadyAddedProject_whenCallPost_thenShouldReturn409(self):
        """ Test add project with already added name"""
        add_project(self, self.authorization)
        with self.client:
            response = add_project(self, self.authorization)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'Project name already exists. Please change the name.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(409, response.status_code)

    def test_givenAlreadyAddedProject_whenCallDelete_thenDeleteSuccessfully(self):
        """ Test delete already added project"""
        response = add_project(self, self.authorization)
        data = json.loads(response.data.decode())
        with self.client:
            response = delete_project(self, data['project_id'], self.authorization)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(
                data['message'] == 'Successfully deleted.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(200, response.status_code)

    def test_givenNonAddedProject_whenCallDelete_thenShouldReturn401(self):
        """ Test delete non added project"""
        with self.client:
            response = delete_project(self, 'fake_projec_id', self.authorization)
            data = json.loads(response.data.decode())
            self.assertEqual('fail', data['status'] )
            self.assertEqual(
                    'Provide a valid project owner auth token.',
                    data['message'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(401, response.status_code)
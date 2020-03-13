import datetime
import json

from project.tests.integration.base import BaseTestCase


def add_project(self):
    return self.client.post(
        '/projects/',
        data=json.dumps(dict(
            name='test project name'
        )),
        content_type='application/json'
    )

def delete_project(self, project_id):
    return self.client.delete(
        '/projects/' + str(project_id),
        content_type='application/json'
    )

def get_project(self, project_id):
    return self.client.get(
        '/projects/' + str(project_id),
        content_type='application/json'
    )

def get_projects(self):
    return self.client.get(
        '/projects/',
        content_type='application/json'
    )


class TestUserController(BaseTestCase):

    def test_givenProjectData_whenCallPost_thenAddTheProject(self):
        """ Test for add project """
        with self.client:
            response = add_project(self)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully added.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(201, response.status_code)

    def test_givenProjectId_whenCallGet_thenGetTheProject(self):
        """ Get a project"""
        response = add_project(self)
        data = json.loads(response.data.decode())
        with self.client:
            response = get_project(self, data['project_id'])
            data = json.loads(response.data.decode())
            self.assertTrue(data['name'] == 'test project name')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(200, response.status_code)

    def test_givenNA_whenCallGet_thenGetAllProject(self):
        """ List all projects"""
        add_project(self)
        with self.client:
            response = get_projects(self)
            data = json.loads(response.data.decode())['data']
            self.assertEqual(1, len(data))
            self.assertEqual('test project name', data[0]['name'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(200, response.status_code)

    def test_givenAlreadyAddedProject_whenCallPost_thenShouldReturn409(self):
        """ Test add project with already added name"""
        add_project(self)
        with self.client:
            response = add_project(self)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'Project name already exists. Please change the name.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(409, response.status_code)

    def test_givenAlreadyAddedProject_whenCallDelete_thenDeleteSuccessfully(self):
        """ Test delete already added project"""
        response = add_project(self)
        data = json.loads(response.data.decode())
        with self.client:
            response = delete_project(self, data['project_id'])
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(
                data['message'] == 'Successfully deleted.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(200, response.status_code)

    def test_givenNonAddedProject_whenCallDelete_thenShouldReturn404(self):
        """ Test delete non added project"""
        with self.client:
            response = delete_project(self, '324234235433453')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'No project found!')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(404, response.status_code)
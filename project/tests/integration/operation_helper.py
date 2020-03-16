import json


def add_project(self, authorization):
    return self.client.post(
        '/projects/',
        data=json.dumps(dict(
            name='test project name'
        )),
        headers={'Authorization': authorization},
        content_type='application/json'
    )


def delete_project(self, project_id, authorization):
    return self.client.delete(
        '/projects/' + str(project_id),
        headers={'Authorization': authorization},
        content_type='application/json'
    )


def get_project(self, project_id, authorization):
    return self.client.get(
        '/projects/' + str(project_id),
        headers={'Authorization': authorization},
        content_type='application/json'
    )


def get_projects(self, authorization):
    return self.client.get(
        '/projects/',
        headers={'Authorization': authorization},
        content_type='application/json'
    )


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


def register_auth_user(self):
    return self.client.post(
        '/users/',
        data=json.dumps(dict(
            email='auth@gmail.com',
            name='name',
            surname='surname',
            password='12345'
        )),
        content_type='application/json'
    )


def register_second_user(self):
    return self.client.post(
        '/users/',
        data=json.dumps(dict(
            email='mesut@gmail.com',
            name='name',
            surname='surname',
            password='12345'
        )),
        content_type='application/json'
    )


def delete_user(self, authorization):
    return self.client.delete(
        '/users/ali@gmail.com',
        headers={'Authorization': authorization},
        content_type='application/json'
    )


def get_a_user(self, authorization):
    return self.client.get(
        '/users/ali@gmail.com',
        headers={'Authorization': authorization},
        content_type='application/json'
    )


def get_users(self, authorization):
    return self.client.get(
        '/users/',
        headers={'Authorization': authorization},
        content_type='application/json'
    )


def add_device(self):
    return self.client.post(
        '/devices/',
        data=json.dumps(dict(
            name='test device name',
            serial_number='12345'
        )),
        headers={'Authorization': self.authorization},
        content_type='application/json'
    )

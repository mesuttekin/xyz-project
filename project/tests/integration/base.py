import json

from flask_testing import TestCase
from project.main import db
from manage import app
from project.tests.integration.operation_helper import register_auth_user


class BaseTestCase(TestCase):
    """ Base Test """
    authorization = ''

    def create_app(self):
        app.config.from_object('project.main.config.TestingConfig')
        return app

    def setUp(self):
        db.drop_all()
        db.create_all()

        response = register_auth_user(self)
        user = json.loads(response.data.decode())
        self.authorization = user['Authorization']

    def tearDown(self):
        db.session.remove()
        db.drop_all()
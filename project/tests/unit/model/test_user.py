import unittest

from flask_testing import TestCase

from manage import app
from project.main.config import basedir
from project.main.model.user import User


class TestUser(TestCase):
    def create_app(self):
        app.config.from_object('project.main.config.TestingConfig')
        return app

    def test_givenUser_when_thenGetUser(self):
        actual_user = User(
            id = "322",
            email='test@test.com',
            name='Mesut',
            surname='Tekin',
            password='test'
        )

        self.assertEqual("322", actual_user.id)
        self.assertEqual("test@test.com", actual_user.email)
        self.assertEqual("Mesut", actual_user.name)
        self.assertEqual("Tekin", actual_user.surname)
        self.assertTrue(actual_user.check_password("test"))

        with self.assertRaises(AttributeError):
            actual_user.password()

if __name__ == "__main__":
    unittest.main(exit=False)
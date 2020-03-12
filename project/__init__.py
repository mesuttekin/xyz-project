# project/__init__.py

from flask_restplus import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.project_controller import api as project_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='XYZ REALITY PROJECT',
          version='1.0',
          description='XYZ Reality user and project web service'
          )

api.add_namespace(user_ns, path='/users')
api.add_namespace(auth_ns)
api.add_namespace(project_ns, path='/projects')

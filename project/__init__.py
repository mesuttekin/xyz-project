# project/__init__.py

from flask import Blueprint
from flask_restplus import Api

from .main.controller.auth_controller import api as auth_ns
from .main.controller.device_controller import api as device_ns
from .main.controller.project_controller import api as project_ns
from .main.controller.project_device_controller import api_device_project as project_device_ns
from .main.controller.project_user_controller import api_user as project_user_ns
from .main.controller.user_controller import api as user_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='XYZ REALITY PROJECT',
          version='1.0',
          description='XYZ Reality user and project web service'
          )

api.add_namespace(user_ns, path='/users')
api.add_namespace(project_ns, path='/projects')
api.add_namespace(device_ns, path='/devices')
api.add_namespace(auth_ns)
api.add_namespace(project_user_ns)
api.add_namespace(project_device_ns)

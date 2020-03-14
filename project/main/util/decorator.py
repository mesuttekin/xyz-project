from functools import wraps
from flask import request

from project.main.service.auth_service import Auth
from project.main.util.security_level import SecurityLevel


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = Auth.get_logged_in_user(request)
        user = data.get('data')

        if not user:
            return data, status

        return f(*args, **kwargs, current_user_email=user['email'])

    return decorated

def project_owner_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = Auth.get_logged_in_user(
            request,
            security_level=SecurityLevel.Project_Owner,
            project_id=kwargs['project_id']
        )

        token = data.get('data')

        if not token:
            return data, status

        return f(*args, **kwargs)

    return decorated



from project.main.model.project_user import ProjectUser
from project.main.model.user import User
from project.main.util.security_level import SecurityLevel


class Auth:

    @staticmethod
    def login_user(data):
        try:
            # fetch the user data
            user = User.query.filter_by(email=data.get('email')).first()
            if user and user.check_password(data.get('password')):
                auth_token = user.encode_auth_token(user.id, user.email)
                if auth_token:
                    response_object = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'Authorization': auth_token.decode()
                    }
                    return response_object, 200
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'email or password does not match.'
                }
                return response_object, 401

        except Exception as e:
            print(e)
            response_object = {
                'status': 'fail',
                'message': 'Try again'
            }
            return response_object, 500

    @staticmethod
    def logout_user(data):
        if data:
            auth_token = data.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                # TODO:Blacklist implementation. Save database and prevent not to use token again
                response_object = {
                    'status': 'success',
                    'message': 'Successfully logged out.'
                }
                return response_object, 200
            else:
                response_object = {
                    'status': 'fail',
                    'message': resp
                }
                return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 403

    @staticmethod
    def get_logged_in_user(new_request, security_level=None, project_id=None):
        # get the auth token
        auth_token = new_request.headers.get('Authorization')
        if auth_token:
            payload = User.decode_auth_token(auth_token)
            if not isinstance(payload, str):
                if security_level == SecurityLevel.Project_Owner:
                    return Auth.get_project_owner_user(payload['user_email'], project_id)
                elif security_level == SecurityLevel.Project_Member:
                    return Auth.get_project_member_user(payload['user_email'], project_id)
                else:
                    return Auth.get_user(payload['user_id']), 200
            response_object = {
                'status': 'fail',
                'message': payload
            }
            return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 401

    @staticmethod
    def get_user(user_id):
        user = User.query.filter_by(id=user_id).first()
        response_object = {
            'status': 'success',
            'data': {
                'user_id': user.id,
                'email': user.email
            }
        }
        return response_object

    @staticmethod
    def get_project_owner_user(user_email, project_id):
        project_user = ProjectUser.query \
            .filter_by(user_email=user_email, project_id=project_id, project_owner=True) \
            .first()
        if project_user:
            response_object = {
                'status': 'success',
                'data': {
                    'email': user_email
                }
            }
            return response_object, 200
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid project owner auth token.'
            }
            return response_object, 401

    @staticmethod
    def get_project_member_user(user_email, project_id):
        project_user = ProjectUser.query \
            .filter_by(user_email=user_email, project_id=project_id) \
            .first()
        if project_user:
            response_object = {
                'status': 'success',
                'data': {
                    'email': user_email
                }
            }
            return response_object, 200
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid project member auth token.'
            }
            return response_object, 401

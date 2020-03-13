
from project.main import db
from project.main.model.project import Project
from project.main.model.project_user import ProjectUser


def save_new_project_user(data):
    project_user = ProjectUser.query.filter_by(user_email=data['user_email'], project_id=data['project_id']).first()
    if not project_user:
        new_project_user = ProjectUser(
            user_email=data['user_email'],
            project_id=data['project_id'],
            project_owner=data['project_owner']
        )
        save_changes(new_project_user)
        response_object = {
            'status': 'success',
            'message': 'Successfully added.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Same user has already assigned to the project.',
        }
        return response_object, 409


def save_changes(project_user):
    db.session.add(project_user)
    db.session.flush()

def get_project_users(project_id):
    return ProjectUser.query.filter_by(project_id=project_id).all()

def get_project_user(project_id, user_email):
    return ProjectUser.query.filter_by(project_id=project_id, user_email=user_email).first()


def delete_project_user(project_id, user_email):
    project_user = ProjectUser.query.filter_by(project_id=project_id, user_email=user_email).first()
    if project_user:
        delete_project_from_db(project_user)
        response_object = {
            'status': 'success',
            'message': 'Successfully deleted.',
            'project_user_id':project_user.id
        }
        return response_object, 200
    else:
        response_object = {
            'status': 'fail',
            'message': "No project user found!",
        }
        return response_object, 404


def delete_project_from_db(project):
    db.session.delete(project)
    db.session.commit()



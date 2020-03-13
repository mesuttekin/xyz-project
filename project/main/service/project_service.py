import datetime

from project.main import db
from project.main.model.project import Project


def save_new_project(data):
    project = Project.query.filter_by(name=data['name']).first()
    if not project:
        new_project = Project(
            name=data['name'],
            created_date=datetime.datetime.utcnow()
        )
        save_changes(new_project)
        response_object = {
            'status': 'success',
            'message': 'Successfully added.',
            'project_id': new_project.id
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Project name already exists. Please change the name.',
        }
        return response_object, 409


def get_user_projects(user_id):
    # TODO: filter with user_id
    return Project.query.all()


def get_project(project_id):
    return Project.query.filter_by(id=project_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.flush()


def delete_project(project_id):
    project = Project.query.filter_by(id=project_id).first()
    if project:
        delete_project_from_db(project)
        response_object = {
            'status': 'success',
            'message': 'Successfully deleted.'
        }
        return response_object, 200
    else:
        response_object = {
            'status': 'fail',
            'message': "No project found!",
        }
        return response_object, 404


def delete_project_from_db(project):
    db.session.delete(project)
    db.session.commit()

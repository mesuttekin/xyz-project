from project.main import db
from project.main.model.user import User


def save_new_user(data):
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        new_user = User(
            email=data['email'],
            name=data['name'],
            surname=data['surname'],
            password=data['password'],
        )
        save_changes(new_user)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409


def get_all_users():
    return User.query.all()


def get_a_user(email):
    return User.query.filter_by(email=email).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()


def delete_user(email):
    user = User.query.filter_by(email=email).first()
    if user:
        delete_user_from_db(user)
        response_object = {
            'status': 'success',
            'message': 'Successfully deleted.'
        }
        return response_object, 200
    else:
        response_object = {
            'status': 'fail',
            'message': "No user found!",
        }
        return response_object, 404


def delete_user_from_db(user):
    db.session.delete(user)
    db.session.commit()

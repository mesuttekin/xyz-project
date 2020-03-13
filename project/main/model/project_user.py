import datetime
import jwt

from .. import db, flask_bcrypt
from ..config import key


class ProjectUser(db.Model):
    """ UserProject Model for storing user's projects """
    __tablename__ = "project-user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    project_id = db.Column(db.Integer, nullable=False)
    project_owner = db.Column(db.Boolean)

import datetime
import jwt

from .. import db, flask_bcrypt
from ..config import key


class ProjectUser(db.Model):
    """ UserProject Model for storing user's projects """
    __tablename__ = "project_user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_email = db.Column(db.String(255))
    project_id = db.Column(db.Integer, nullable=False)
    project_owner = db.Column(db.Boolean)

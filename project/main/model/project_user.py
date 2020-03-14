from .. import db


class ProjectUser(db.Model):
    """ UserProject Model for storing user's projects """
    __tablename__ = "project_user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_email = db.Column(db.String(255), db.ForeignKey('user.email'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    project_owner = db.Column(db.Boolean)
    project = db.relationship('Project', foreign_keys=project_id)

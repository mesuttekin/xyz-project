from .. import db

class Project(db.Model):
    """ Project Model for storing project related info """
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False)

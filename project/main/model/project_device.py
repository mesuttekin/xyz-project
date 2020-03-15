from .. import db


class ProjectDevice(db.Model):
    """ Device Model for storing device related info """
    __tablename__ = "project_device"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, nullable=False)
    device_id = db.Column(db.Integer)
    created_date = db.Column(db.DateTime, nullable=False)

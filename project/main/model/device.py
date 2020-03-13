from .. import db

class Device(db.Model):
    """ Device Model for storing device related info """
    __tablename__ = "device"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    serial_number = db.Column(db.String(5), nullable=False)
    project_id = db.Column(db.Integer)
    created_date = db.Column(db.DateTime, nullable=False)

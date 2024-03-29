from sqlalchemy_utils import UUIDType

from .mixins import BaseMixin
from .. import db


class Hole(db.Model, BaseMixin):
    # Constraints
    __table_args__ = (db.UniqueConstraint('course_uuid', 'number', name='course_hole_number'),)

    name = db.Column(db.String, nullable=True)
    number = db.Column(db.Integer, nullable=False)
    par = db.Column(db.Integer, nullable=False)
    distance = db.Column(db.Integer, nullable=False)

    # FK
    course_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('course.uuid'), nullable=True)

    # Relationship
    course = db.relationship("Course", back_populates="holes")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Hole.register()

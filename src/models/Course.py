from sqlalchemy_utils import CountryType
from sqlalchemy_utils.types import TSVectorType

from .mixins import BaseMixin
from .. import db
from ..common import StatusEnum


class Course(db.Model, BaseMixin):
    name = db.Column(db.String, nullable=False)
    status = db.Column(db.Enum(StatusEnum), nullable=False)
    line_1 = db.Column(db.String, nullable=True)
    line_2 = db.Column(db.String, nullable=True)
    city = db.Column(db.String, nullable=True)
    province = db.Column(db.String, nullable=True)
    country = db.Column(CountryType, nullable=True)

    # Search
    search_vector = db.Column(
        TSVectorType('name', 'city', 'country', weights={'name': 'A', 'city': 'B', 'country': 'C'}))

    # Relationship
    holes = db.relationship("Hole", back_populates="course")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Course.register()

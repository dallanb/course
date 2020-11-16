from sqlalchemy_utils import EmailType, PhoneNumber, CountryType, URLType

from .mixins import BaseMixin
from .. import db
from ..common import StatusEnum


class Course(db.Model, BaseMixin):
    name = db.Column(db.String, nullable=False)
    status = db.Column(db.Enum(StatusEnum), nullable=False)
    email = db.Column(EmailType, unique=True, nullable=True)
    _number = db.Column(db.Unicode(20), nullable=True)
    country_code = db.Column(db.Unicode(8), nullable=True)
    extension = db.Column(db.Unicode(20), nullable=True)

    number = db.composite(
        PhoneNumber,
        _number,
        country_code
    )
    line_1 = db.Column(db.String, nullable=True)
    line_2 = db.Column(db.String, nullable=True)
    city = db.Column(db.String, nullable=True)
    province = db.Column(db.String, nullable=True)
    country = db.Column(CountryType, nullable=True)
    postal_code = db.Column(db.String, nullable=True)
    website = db.Column(URLType, nullable=True)

    # Relationship
    holes = db.relationship("Hole", back_populates="course")

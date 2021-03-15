from .schema import CourseApprovedSchema
from ..base import Base


class course_approved(Base):
    key = 'course_approved'
    schema = CourseApprovedSchema()

    def __init__(self, data):
        super().__init__(key=self.key, data=data)

    @classmethod
    def from_data(cls, course):
        data = cls.schema.dump({'course': course})
        return course_approved(data=data)

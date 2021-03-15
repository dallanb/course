from .schema import CourseCreatedSchema
from ..base import Base


class course_created(Base):
    key = 'course_created'
    schema = CourseCreatedSchema()

    def __init__(self, data):
        super().__init__(key=self.key, data=data)

    @classmethod
    def from_data(cls, course):
        data = cls.schema.dump({'course': course})
        return course_created(data=data)

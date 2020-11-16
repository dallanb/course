import logging
from http import HTTPStatus

from .base import Base
from ..models import Course as CourseModel


class Course(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.course_model = CourseModel

    def find(self, **kwargs):
        return Base.find(self, model=self.course_model, **kwargs)

    def create(self, **kwargs):
        course = self.init(model=self.course_model, **kwargs)
        return self.save(instance=course)

    def update(self, uuid, **kwargs):
        courses = self.find(uuid=uuid)
        if not courses.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return self.apply(instance=courses.items[0], **kwargs)

    def apply(self, instance, **kwargs):
        # if course status is being updated we will trigger a notification
        course = self.assign_attr(instance=instance, attr=kwargs)
        return self.save(instance=course)

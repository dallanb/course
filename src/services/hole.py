import logging
from http import HTTPStatus

from .base import Base
from ..models import Hole as HoleModel


class Hole(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.hole_model = HoleModel

    def find(self, **kwargs):
        return Base.find(self, model=self.hole_model, **kwargs)

    def create(self, **kwargs):
        hole = self.init(model=self.hole_model, **kwargs)
        return self.save(instance=hole)

    def update(self, uuid, **kwargs):
        holes = self.find(uuid=uuid)
        if not holes.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return self.apply(instance=holes.items[0], **kwargs)

    def apply(self, instance, **kwargs):
        hole = self.assign_attr(instance=instance, attr=kwargs)
        return self.save(instance=hole)

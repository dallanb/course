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
        return self._find(model=self.hole_model, **kwargs)

    def create(self, **kwargs):
        hole = self._init(model=self.hole_model, **kwargs)
        return self._save(instance=hole)

    def add(self, **kwargs):
        hole = self._init(model=self.hole_model, **kwargs)
        return self._add(instance=hole)

    def commit(self):
        return self._commit()

    def update(self, uuid, **kwargs):
        holes = self.find(uuid=uuid)
        if not holes.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return self.apply(instance=holes.items[0], **kwargs)

    def apply(self, instance, **kwargs):
        hole = self._assign_attr(instance=instance, attr=kwargs)
        return self._save(instance=hole)

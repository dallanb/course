from flask import request
from flask_restful import marshal_with

from .schema import *
from ..base import Base
from ....common.response import DataResponse
from ....services import Hole, Course


class HolesAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.hole = Hole()

    @marshal_with(DataResponse.marshallable())
    def get(self, uuid):
        holes = self.hole.find(uuid=uuid)
        if not holes.total:
            self.throw_error(http_code=self.code.NOT_FOUND)
        return DataResponse(
            data={
                'holes': self.dump(
                    schema=dump_schema,
                    instance=holes.items[0]
                )
            }
        )

    @marshal_with(DataResponse.marshallable())
    def put(self, uuid):
        data = self.clean(schema=update_schema, instance=request.get_json())
        hole = self.hole.update(uuid=uuid, **data)
        return DataResponse(
            data={
                'holes': self.dump(
                    schema=dump_schema,
                    instance=hole
                )
            }
        )


class HolesListAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.hole = Hole()
        self.course = Course()

    @marshal_with(DataResponse.marshallable())
    def get(self):
        data = self.clean(schema=fetch_all_schema, instance=request.args)
        holes = self.hole.find(**data)
        return DataResponse(
            data={
                '_metadata': self.prepare_metadata(
                    total_count=holes.total,
                    page_count=len(holes.items),
                    page=data['page'],
                    per_page=data['per_page']
                ),
                'holes': self.dump(
                    schema=dump_many_schema,
                    instance=holes.items,
                )
            }
        )

    @marshal_with(DataResponse.marshallable())
    def post(self, uuid):
        data = self.clean(schema=create_schema, instance=request.get_json())
        courses = self.course.find(uuid=uuid)
        if not courses.total:
            self.throw_error(http_code=self.code.NOT_FOUND)
        hole = self.hole.create(course=courses.items[0], **data)
        return DataResponse(
            data={
                'holes': self.dump(
                    schema=dump_schema,
                    instance=hole
                )
            }
        )

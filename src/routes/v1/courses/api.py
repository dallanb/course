from flask import request, g
from flask_restful import marshal_with

from .schema import *
from ..base import Base
from ....common import check_user
from ....common.response import DataResponse
from ....services import CourseService, HoleService


class CoursesAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.course = CourseService()

    @marshal_with(DataResponse.marshallable())
    def get(self, uuid):
        courses = self.course.find(uuid=uuid)
        if not courses.total:
            self.throw_error(http_code=self.code.NOT_FOUND)
        return DataResponse(
            data={
                'courses': self.dump(
                    schema=dump_schema,
                    instance=courses.items[0]
                )
            }
        )

    @marshal_with(DataResponse.marshallable())
    def put(self, uuid):
        data = self.clean(schema=update_schema, instance=request.get_json())
        course = self.course.update(uuid=uuid, **data)
        return DataResponse(
            data={
                'courses': self.dump(
                    schema=dump_schema,
                    instance=course
                )
            }
        )


class CoursesListAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.course = CourseService()
        self.hole = HoleService()

    @marshal_with(DataResponse.marshallable())
    def get(self):
        data = self.clean(schema=fetch_all_schema, instance=request.args)
        courses = self.course.find(**data)
        return DataResponse(
            data={
                '_metadata': self.prepare_metadata(
                    total_count=courses.total,
                    page_count=len(courses.items),
                    page=data['page'],
                    per_page=data['per_page']),
                'courses': self.dump(
                    schema=dump_many_schema,
                    instance=courses.items
                )
            }
        )

    @marshal_with(DataResponse.marshallable())
    @check_user
    def post(self):
        data = self.clean(schema=create_schema, instance=request.get_json())
        holes = data.pop('holes', None)
        course = self.course.create(status='pending', **data, created_by=g.user)

        if holes is not None:
            for hole in holes:
                self.hole.add(course=course, **hole)
            self.hole.commit()
        return DataResponse(
            data={
                'courses': self.dump(
                    schema=dump_schema,
                    instance=course
                )
            }
        )

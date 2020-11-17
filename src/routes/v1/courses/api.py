from flask import request
from flask_restful import marshal_with

from .schema import *
from ..base import Base
from ....common.response import DataResponse
from ....services import Course


class CoursesAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.course = Course()

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


class CoursesListAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.course = Course()

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
    def post(self):
        data = self.clean(schema=create_schema, instance=request.get_json())
        course = self.course.create(status='pending', **data)

        # participants = data.pop('participants')
        # if participants:
        #     for user_uuid in participants:
        #         status = 'active' if g.user == user_uuid else 'pending'
        #         self.participant.create(user_uuid=user_uuid, status=status, contest=contest)
        return DataResponse(
            data={
                'courses': self.dump(
                    schema=dump_schema,
                    instance=course
                )
            }
        )


class CoursesListSearchAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.course = Course()

    @marshal_with(DataResponse.marshallable())
    def get(self):
        data = self.clean(schema=search_schema, instance=request.args)
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

from marshmallow import Schema, pre_dump
from webargs import fields


class CourseApprovedSchema(Schema):
    uuid = fields.UUID(attribute='course.uuid')
    created_by = fields.UUID(attribute='course.league_uuid')
    message = fields.String()

    @pre_dump
    def prepare(self, data, **kwargs):
        course = data['course']
        data['message'] = f"{course.name} has been approved"
        return data

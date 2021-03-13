from marshmallow import Schema
from webargs import fields


class CourseApprovedSchema(Schema):
    uuid = fields.UUID(attribute='course.uuid')
    created_by = fields.UUID(attribute='course.league_uuid')

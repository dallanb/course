from marshmallow import Schema
from webargs import fields


class CourseCreatedSchema(Schema):
    uuid = fields.UUID(attribute='course.uuid')
    created_by = fields.UUID(attribute='course.created_by')

from marshmallow import Schema
from webargs import fields


class CreateHoleSchema(Schema):
    name = fields.String(required=False)
    number = fields.Integer(required=True)
    par = fields.Integer(required=True)
    distance = fields.Integer(required=True)


class DumpHoleSchema(Schema):
    uuid = fields.UUID()
    course_uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()
    name = fields.String()
    number = fields.Integer()
    par = fields.Integer()
    distance = fields.Integer()


class FetchAllHoleSchema(Schema):
    page = fields.Int(required=False, missing=1)
    per_page = fields.Int(required=False, missing=10)


class UpdateHoleSchema(Schema):
    name = fields.String(required=False)
    number = fields.Integer(required=False)
    par = fields.Integer(required=False)
    distance = fields.Integer(required=False)


create_schema = CreateHoleSchema()
dump_schema = DumpHoleSchema()
dump_many_schema = DumpHoleSchema(many=True)
fetch_all_schema = FetchAllHoleSchema()
update_schema = UpdateHoleSchema()

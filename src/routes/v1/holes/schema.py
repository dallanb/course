from marshmallow import Schema, post_dump
from webargs import fields


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


dump_schema = DumpHoleSchema()
dump_many_schema = DumpHoleSchema(many=True)
fetch_all_schema = FetchAllHoleSchema()

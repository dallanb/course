from marshmallow import Schema, post_dump
from marshmallow_enum import EnumField
from webargs import fields

from src.common import StatusEnum


class CreateCourseSchema(Schema):
    name = fields.String(required=True)
    line_1 = fields.Str(required=False, missing=None)
    line_2 = fields.Str(required=False, missing=None)
    city = fields.Str(required=False, missing=None)
    province = fields.Str(required=False, missing=None)
    country = fields.Str(required=False, missing=None)


class DumpCourseSchema(Schema):
    uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()
    name = fields.String()
    status = EnumField(StatusEnum)
    line_1 = fields.String()
    line_2 = fields.String()
    city = fields.String()
    province = fields.String()
    country = fields.String()
    holes = fields.List(fields.Nested('DumpHoleSchema'))

    def get_attribute(self, obj, attr, default):
        if attr == 'country':
            return obj.country.code if getattr(obj, 'country', None) else default
        return getattr(obj, attr, default)

    @post_dump
    def make_obj(self, data, **kwargs):
        return data


class FetchAllCourseSchema(Schema):
    page = fields.Int(required=False, missing=1)
    per_page = fields.Int(required=False, missing=10)
    name = fields.String(required=False)


class UpdateCourseSchema(Schema):
    name = fields.String(required=False)
    line_1 = fields.Str(required=False, missing=None)
    line_2 = fields.Str(required=False, missing=None)
    city = fields.Str(required=False, missing=None)
    province = fields.Str(required=False, missing=None)
    country = fields.Str(required=False, missing=None)


class SearchCourseSchema(Schema):
    page = fields.Int(required=False, missing=1)
    per_page = fields.Int(required=False, missing=10)
    key = fields.String(attribute='search.key', data_key='key')
    fields = fields.DelimitedList(fields.String(), attribute='search.fields', data_key='fields')


create_schema = CreateCourseSchema()
dump_schema = DumpCourseSchema()
dump_many_schema = DumpCourseSchema(many=True)
fetch_all_schema = FetchAllCourseSchema()
update_schema = UpdateCourseSchema()
search_schema = SearchCourseSchema()
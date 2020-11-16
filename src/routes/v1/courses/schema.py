from marshmallow import validate, Schema, post_dump
from marshmallow_enum import EnumField
from webargs import fields

from src.common import StatusEnum


class DumpCoursesSchema(Schema):
    uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()
    name = fields.String()
    status = EnumField(StatusEnum)
    email = fields.Email()
    number = fields.String()
    country_code = fields.String()
    extension = fields.String()
    line_1 = fields.String()
    line_2 = fields.String()
    city = fields.String()
    province = fields.String()
    country = fields.String()
    postal_code = fields.String()
    holes = fields.List(fields.Nested('DumpHoleSchema'))

    def get_attribute(self, obj, attr, default):
        if attr == 'country':
            return obj.country.code if getattr(obj, 'country', None) else default
        return getattr(obj, attr, default)

    @post_dump
    def make_obj(self, data, **kwargs):
        return data


class FetchAllCoursesSchema(Schema):
    page = fields.Int(required=False, missing=1)
    per_page = fields.Int(required=False, missing=10)
    name = fields.String(required=False)


class SearchCourseSchema(Schema):
    page = fields.Int(required=False, missing=1)
    per_page = fields.Int(required=False, missing=10)
    key = fields.String(attribute='search.key', data_key='key')
    fields = fields.DelimitedList(fields.String(), attribute='search.fields', data_key='fields')


dump_schema = DumpCoursesSchema()
dump_many_schema = DumpCoursesSchema(many=True)
fetch_all_schema = FetchAllCoursesSchema()
search_schema = SearchCourseSchema()

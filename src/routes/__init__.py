from .. import api
from .v1 import PingAPI
from .v1 import CoursesAPI, CoursesListAPI, CoursesListSearchAPI

# Ping
api.add_resource(PingAPI, '/ping', methods=['GET'])

# Contests
api.add_resource(CoursesAPI, '/courses/<uuid:uuid>', endpoint="course")
api.add_resource(CoursesListAPI, '/courses', endpoint="courses")
api.add_resource(CoursesListSearchAPI, '/courses/search', endpoint="courses_search")

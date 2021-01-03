from .. import api
from .v1 import PingAPI
from .v1 import CoursesAPI, CoursesListAPI
from .v1 import HolesAPI, HolesListAPI

# Ping
api.add_resource(PingAPI, '/ping', methods=['GET'])

# Contests
api.add_resource(CoursesAPI, '/courses/<uuid:uuid>', endpoint="course")
api.add_resource(CoursesListAPI, '/courses', endpoint="courses")

# Holes
api.add_resource(HolesAPI, '/holes/<uuid:uuid>', endpoint="hole")
api.add_resource(HolesListAPI, '/courses/<uuid:uuid>/holes', '/holes', endpoint="holes")

from uuid import uuid4

import pytest

from .fixtures import *


def pytest_configure(config):
    pytest.course = None
    pytest.hole = None
    pytest.course_name = 'Northlands Golf Course'
    pytest.line_1 = '3400 Anne Macdonald Way'
    pytest.line_2 = None
    pytest.city = 'North Vancouver'
    pytest.province = 'British Columbia'
    pytest.country = 'CA'
    pytest.hole_name = 'Uno'
    pytest.hole_number = 1
    pytest.par = 3
    pytest.distance = 345
    pytest.user_uuid = uuid4()

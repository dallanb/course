from uuid import uuid4

import pytest

from .fixtures import *

def pytest_configure(config):
    pytest.course = None
    pytest.course_name = 'Northlands Golf Course'
    pytest.line_1 = '3400 Anne Macdonald Way'
    pytest.line_2 = None
    pytest.city = 'North Vancouver'
    pytest.province = 'British Columbia'
    pytest.country = 'CA'
    pytest.user_uuid = uuid4()
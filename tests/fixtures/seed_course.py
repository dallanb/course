import pytest

from src import services


@pytest.fixture
def seed_course():
    pytest.course = services.CourseService().create(
        name=pytest.course_name,
        line_1=pytest.line_1,
        line_2=pytest.line_2,
        city=pytest.city,
        province=pytest.province,
        country=pytest.country,
        status='pending'
    )

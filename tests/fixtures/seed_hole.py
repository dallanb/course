import pytest

from src import services


@pytest.fixture
def seed_hole():
    pytest.hole = services.HoleService().create(
        name=pytest.hole_name,
        number=pytest.hole_number,
        par=pytest.par,
        distance=pytest.distance,
        course=pytest.course
    )

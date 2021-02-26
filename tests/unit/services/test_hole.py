import pytest

from src import services, ManualException, app
from tests.helpers import generate_uuid

hole_service = services.HoleService()


###########
# Find
###########
def test_hole_find(reset_db, seed_course, seed_hole):
    """
    GIVEN 1 hole instance in the database
    WHEN the find method is called
    THEN it should return 1 hole
    """

    holes = hole_service.find()
    assert holes.total == 1
    assert len(holes.items) == 1
    hole = holes.items[0]
    assert hole.uuid == pytest.hole.uuid


def test_hole_find_by_uuid():
    """
    GIVEN 1 hole instance in the database
    WHEN the find method is called with uuid
    THEN it should return 1 hole
    """
    hole = pytest.hole
    uuid = hole.uuid

    holes = hole_service.find(uuid=uuid)
    assert holes.total == 1
    assert len(holes.items) == 1
    hole = holes.items[0]
    assert hole.uuid == uuid


def test_hole_find_by_name():
    """
    GIVEN 1 hole instance in the database
    WHEN the find method is called with name
    THEN it should return 1 hole
    """
    hole = pytest.hole
    name = hole.name

    holes = hole_service.find(name=name)
    assert holes.total == 1
    assert len(holes.items) == 1
    hole = holes.items[0]
    assert hole.name == name


def test_hole_find_w_pagination():
    """
    GIVEN 2 hole instance in the database
    WHEN the find method is called with valid pagination
    THEN it should return the number of holes defined in the pagination arguments
    """
    hole_service.create(name='Deuce', number=2, par=4, distance=430, course=pytest.course)

    holes_0 = hole_service.find(page=1, per_page=1)
    assert holes_0.total == 2
    assert len(holes_0.items) == 1

    holes_1 = hole_service.find(page=2, per_page=1)
    assert holes_1.total == 2
    assert len(holes_1.items) == 1
    assert holes_1.items[0] != holes_0.items[0]

    holes = hole_service.find(page=1, per_page=2)
    assert holes.total == 2
    assert len(holes.items) == 2


def test_hole_find_w_bad_pagination():
    """
    GIVEN 2 hole instance in the database
    WHEN the find method is called with invalid pagination
    THEN it should return the 0 hole
    """
    holes = hole_service.find(page=3, per_page=3)
    assert holes.total == 2
    assert len(holes.items) == 0


def test_hole_find_by_name_none_found():
    """
    GIVEN 2 hole instance in the database
    WHEN the find method is called with a random name
    THEN it should return the 0 hole
    """
    holes = hole_service.find(name='Bingo')
    assert holes.total == 0
    assert len(holes.items) == 0


def test_hole_find_by_non_existent_column():
    """
    GIVEN 2 hole instance in the database
    WHEN the find method is called with a random column
    THEN it should return the 0 hole and ManualException with code 400
    """
    try:
        _ = hole_service.find(junk=generate_uuid())
    except ManualException as ex:
        assert ex.code == 400


def test_hole_find_by_non_existent_include():
    """
    GIVEN 2 hole instance in the database
    WHEN the find method is called with a random include
    THEN it should return the 0 hole and ManualException with code 400
    """
    try:
        _ = hole_service.find(include=['junk'])
    except ManualException as ex:
        assert ex.code == 400


def test_hole_find_by_non_existent_expand():
    """
    GIVEN 2 hole instance in the database
    WHEN the find method is called with a random expand
    THEN it should return the 0 hole and ManualException with code 400
    """
    try:
        _ = hole_service.find(expand=['junk'])
    except ManualException as ex:
        assert ex.code == 400


###########
# Create
###########
def test_hole_create(reset_db, seed_course):
    """
    GIVEN 0 hole instance in the database
    WHEN the create method is called
    THEN it should return 1 hole and add 1 hole instance into the database
    """
    hole = hole_service.create(name=pytest.hole_name,
                               number=pytest.hole_number,
                               par=pytest.par,
                               distance=pytest.distance,
                               course=pytest.course)

    assert hole.uuid is not None
    assert hole.name == pytest.hole_name


def test_hole_create_dup():
    """
    GIVEN 1 hole instance in the database
    WHEN the create method is called with the exact same parameters of an existing hole
    THEN it should return 0 hole and add 0 hole instance into the database and ManualException with code 500
    """
    try:
        _ = hole_service.create(name=pytest.hole_name,
                                number=pytest.hole_number,
                                par=pytest.par,
                                distance=pytest.distance,
                                course=pytest.course)
    except ManualException as ex:
        assert ex.code == 500


def test_hole_create_w_bad_field():
    """
    GIVEN 1 hole instance in the database
    WHEN the create method is called with a non existent field
    THEN it should return 0 hole and add 0 hole instance into the database and ManualException with code 500
    """
    try:
        _ = hole_service.create(name=pytest.hole_name,
                                number=pytest.hole_number,
                                par=pytest.par,
                                distance=pytest.distance,
                                course=pytest.course, junk='junk')
    except ManualException as ex:
        assert ex.code == 500


###########
# Update
###########
def test_hole_update(reset_db, seed_course, seed_hole):
    """
    GIVEN 1 hole instance in the database
    WHEN the update method is called
    THEN it should return 1 hole and update 1 hole instance into the database
    """
    hole = hole_service.update(uuid=pytest.hole.uuid, name='Bingo')
    assert hole.uuid is not None

    holes = hole_service.find(uuid=hole.uuid)
    assert holes.total == 1
    assert len(holes.items) == 1


def test_hole_update_w_bad_uuid(reset_db, seed_course, seed_hole):
    """
    GIVEN 1 hole instance in the database
    WHEN the update method is called with random uuid
    THEN it should return 0 hole and update 0 hole instance into the database and ManualException with code 404
    """
    try:
        _ = hole_service.update(uuid=generate_uuid(), name='Ringo')
    except ManualException as ex:
        assert ex.code == 404


def test_hole_update_w_bad_field():
    """
    GIVEN 1 hole instance in the database
    WHEN the update method is called with bad field
    THEN it should return 0 hole and update 0 hole instance in the database and ManualException with code 400
    """
    try:
        _ = hole_service.update(uuid=pytest.hole.uuid, junk='junk')
    except ManualException as ex:
        assert ex.code == 400


###########
# Apply
###########
def test_hole_apply(reset_db, seed_course, seed_hole):
    """
    GIVEN 1 hole instance in the database
    WHEN the apply method is called
    THEN it should return 1 hole and update 1 hole instance in the database
    """
    hole = hole_service.apply(instance=pytest.hole, name='Bingo')
    assert hole.uuid is not None

    holes = hole_service.find(uuid=hole.uuid)
    assert holes.total == 1
    assert len(holes.items) == 1


def test_hole_apply_w_bad_hole(reset_db, seed_course, seed_hole):
    """
    GIVEN 1 hole instance in the database
    WHEN the apply method is called with random uuid
    THEN it should return 0 hole and update 0 hole instance in the database and ManualException with code 404
    """
    try:
        _ = hole_service.apply(instance=generate_uuid(), name='Ringo')
    except ManualException as ex:
        assert ex.code == 400


def test_hole_apply_w_bad_field():
    """
    GIVEN 1 hole instance in the database
    WHEN the apply method is called with bad field
    THEN it should return 0 hole and update 0 hole instance in the database and ManualException with code 400
    """
    try:
        _ = hole_service.apply(instance=pytest.hole, junk='junk')
    except ManualException as ex:
        assert ex.code == 400

import pytest

from src import services, ManualException, app
from tests.helpers import generate_uuid

course_service = services.CourseService()


###########
# Find
###########
def test_course_find(reset_db, seed_course):
    """
    GIVEN 1 course instance in the database
    WHEN the find method is called
    THEN it should return 1 course
    """

    courses = course_service.find()
    assert courses.total == 1
    assert len(courses.items) == 1
    course = courses.items[0]
    assert course.uuid == pytest.course.uuid


def test_course_find_by_uuid():
    """
    GIVEN 1 course instance in the database
    WHEN the find method is called with uuid
    THEN it should return 1 course
    """
    course = pytest.course
    uuid = course.uuid

    courses = course_service.find(uuid=uuid)
    assert courses.total == 1
    assert len(courses.items) == 1
    course = courses.items[0]
    assert course.uuid == uuid


def test_course_find_by_name():
    """
    GIVEN 1 course instance in the database
    WHEN the find method is called with name
    THEN it should return 1 course
    """
    course = pytest.course
    name = course.name

    courses = course_service.find(name=name)
    assert courses.total == 1
    assert len(courses.items) == 1
    course = courses.items[0]
    assert course.name == name


def test_course_find_include_holes(seed_hole):
    """
    GIVEN 1 course instance in the database
    WHEN the find method is called with include argument to also return holes
    THEN it should return 1 course
    """
    courses = course_service.find(include=['holes'])
    assert courses.total == 1
    assert len(courses.items) == 1
    course = courses.items[0]
    assert course.holes is not None


def test_course_find_w_pagination():
    """
    GIVEN 2 course instance in the database
    WHEN the find method is called with valid pagination
    THEN it should return the number of courses defined in the pagination arguments
    """
    course_service.create(status='pending', name=pytest.course_name)

    courses_0 = course_service.find(page=1, per_page=1)
    assert courses_0.total == 2
    assert len(courses_0.items) == 1

    courses_1 = course_service.find(page=2, per_page=1)
    assert courses_1.total == 2
    assert len(courses_1.items) == 1
    assert courses_1.items[0] != courses_0.items[0]

    courses = course_service.find(page=1, per_page=2)
    assert courses.total == 2
    assert len(courses.items) == 2


def test_course_find_w_bad_pagination():
    """
    GIVEN 2 course instance in the database
    WHEN the find method is called with invalid pagination
    THEN it should return the 0 course
    """
    courses = course_service.find(page=3, per_page=3)
    assert courses.total == 2
    assert len(courses.items) == 0


def test_course_find_by_name_none_found():
    """
    GIVEN 2 course instance in the database
    WHEN the find method is called with a random name
    THEN it should return the 0 course
    """
    courses = course_service.find(name='Bingo')
    assert courses.total == 0
    assert len(courses.items) == 0


def test_course_find_by_non_existent_column():
    """
    GIVEN 2 course instance in the database
    WHEN the find method is called with a random column
    THEN it should return the 0 course and ManualException with code 400
    """
    try:
        _ = course_service.find(junk=generate_uuid())
    except ManualException as ex:
        assert ex.code == 400


def test_course_find_by_non_existent_include():
    """
    GIVEN 2 course instance in the database
    WHEN the find method is called with a random include
    THEN it should return the 0 course and ManualException with code 400
    """
    try:
        _ = course_service.find(include=['junk'])
    except ManualException as ex:
        assert ex.code == 400


def test_course_find_by_non_existent_expand():
    """
    GIVEN 2 course instance in the database
    WHEN the find method is called with a random expand
    THEN it should return the 0 course and ManualException with code 400
    """
    try:
        _ = course_service.find(expand=['junk'])
    except ManualException as ex:
        assert ex.code == 400


###########
# Create
###########
def test_course_create(reset_db):
    """
    GIVEN 0 course instance in the database
    WHEN the create method is called
    THEN it should return 1 course and add 1 course instance into the database
    """
    course = course_service.create(status='pending', name=pytest.course_name)

    assert course.uuid is not None
    assert course.name == pytest.course_name


def test_course_create_dup():
    """
    GIVEN 1 course instance in the database
    WHEN the create method is called with the exact same parameters of an existing course
    THEN it should return 1 course and add 1 course instance into the database
    """
    course = course_service.create(status='pending', name=pytest.course_name)
    assert course.uuid is not None


def test_course_create_w_bad_field():
    """
    GIVEN 1 course instance in the database
    WHEN the create method is called with a non existent field
    THEN it should return 0 course and add 0 course instance into the database and ManualException with code 500
    """
    try:
        _ = course_service.create(status='pending', name=pytest.course_name, junk='junk')
    except ManualException as ex:
        assert ex.code == 500


###########
# Update
###########
def test_course_update(reset_db, seed_course):
    """
    GIVEN 1 course instance in the database
    WHEN the update method is called
    THEN it should return 1 course and update 1 course instance into the database
    """
    course = course_service.update(uuid=pytest.course.uuid, name='Bingo')
    assert course.uuid is not None

    courses = course_service.find(uuid=course.uuid)
    assert courses.total == 1
    assert len(courses.items) == 1


def test_course_update_w_bad_uuid(reset_db, seed_course):
    """
    GIVEN 1 course instance in the database
    WHEN the update method is called with random uuid
    THEN it should return 0 course and update 0 course instance into the database and ManualException with code 404
    """
    try:
        _ = course_service.update(uuid=generate_uuid(), name='Ringo')
    except ManualException as ex:
        assert ex.code == 404


def test_course_update_w_bad_field():
    """
    GIVEN 1 course instance in the database
    WHEN the update method is called with bad field
    THEN it should return 0 course and update 0 course instance in the database and ManualException with code 400
    """
    try:
        _ = course_service.update(uuid=pytest.course.uuid, junk='junk')
    except ManualException as ex:
        assert ex.code == 400


###########
# Apply
###########
def test_course_apply(reset_db, seed_course):
    """
    GIVEN 1 course instance in the database
    WHEN the apply method is called
    THEN it should return 1 course and update 1 course instance in the database
    """
    course = course_service.apply(instance=pytest.course, name='Bingo')
    assert course.uuid is not None

    courses = course_service.find(uuid=course.uuid)
    assert courses.total == 1
    assert len(courses.items) == 1


def test_course_apply_w_bad_course(reset_db, seed_course):
    """
    GIVEN 1 course instance in the database
    WHEN the apply method is called with random uuid
    THEN it should return 0 course and update 0 course instance in the database and ManualException with code 404
    """
    try:
        _ = course_service.apply(instance=generate_uuid(), name='Ringo')
    except ManualException as ex:
        assert ex.code == 400


def test_course_apply_w_bad_field():
    """
    GIVEN 1 course instance in the database
    WHEN the apply method is called with bad field
    THEN it should return 0 course and update 0 course instance in the database and ManualException with code 400
    """
    try:
        _ = course_service.apply(instance=pytest.course, junk='junk')
    except ManualException as ex:
        assert ex.code == 400

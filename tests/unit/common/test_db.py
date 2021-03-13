import pytest

from src import services
from src.common import DB, Cleaner
from src.models import *
from tests.helpers import generate_uuid

db = DB()
cleaner = Cleaner()


def test_init(reset_db):
    """
    GIVEN a db instance
    WHEN calling the init method of the db instance on the Course model
    THEN it should return the course instance
    """
    instance = db.init(model=Course, name=pytest.course_name, created_by=pytest.user_uuid, status='pending')
    assert cleaner.is_mapped(instance) == instance
    assert cleaner.is_uuid(instance.uuid) is not None
    assert instance.name == pytest.course_name

    db.rollback()


def test_count():
    """
    GIVEN a db instance
    WHEN calling the count method of the db instance on the Course model
    THEN it should return the number of course instances
    """
    count = db.count(model=Course)
    assert count == 0

    course = db.init(model=Course, name=pytest.course_name, created_by=pytest.user_uuid, status='pending')
    _ = db.save(instance=course)
    count = db.count(model=Course)
    assert count == 1


def test_add(reset_db):
    """
    GIVEN a db instance
    WHEN calling the add method of the db instance on a course instance
    THEN it should add a course instance to the database
    """
    instance = db.init(model=Course, name=pytest.course_name, created_by=pytest.user_uuid, status='pending')
    course = db.add(instance=instance)
    assert cleaner.is_uuid(course.uuid) is not None
    assert course.name == pytest.course_name

    db.rollback()
    assert db.count(model=Course) == 0


def test_commit(reset_db):
    """
    GIVEN a db instance
    WHEN calling the commit method of the db instance on a course instance
    THEN it should add a course instance to the database
    """
    instance = db.init(model=Course, name=pytest.course_name, created_by=pytest.user_uuid, status='pending')
    course = db.add(instance=instance)
    assert cleaner.is_uuid(course.uuid) is not None
    assert course.name == pytest.course_name

    db.rollback()
    assert db.count(model=Course) == 0

    _ = db.add(instance=instance)
    db.commit()
    assert db.count(model=Course) == 1

    instance_0 = db.init(model=Course, name='A', created_by=pytest.user_uuid, status='pending')
    instance_1 = db.init(model=Course, name='B', created_by=pytest.user_uuid, status='pending')
    instance_2 = db.init(model=Course, name='C', created_by=pytest.user_uuid, status='pending')
    db.add(instance=instance_0)
    db.add(instance=instance_1)
    db.add(instance=instance_2)
    db.commit()
    assert db.count(model=Course) == 4


def test_save(reset_db):
    """
    GIVEN a db instance
    WHEN calling the save method of the db instance on a course instance
    THEN it should add a course instance to the database
    """
    instance = db.init(model=Course, name=pytest.course_name, created_by=pytest.user_uuid, status='pending')
    assert cleaner.is_uuid(instance.uuid) is not None
    assert instance.name == pytest.course_name
    course = db.save(instance=instance)
    assert db.count(model=Course) == 1
    assert course.name == pytest.course_name


def test_find():
    """
    GIVEN a db instance
    WHEN calling the find method of the db instance
    THEN it should find a course instance from the database
    """
    result = db.find(model=Course)
    assert result.total == 1
    assert len(result.items) == 1

    result = db.find(model=Course, uuid=generate_uuid())
    assert result.total == 0


def test_destroy():
    """
    GIVEN a db instance
    WHEN calling the destroy method of the db instance on a course instance
    THEN it should remove the course instance from the database
    """
    result = db.find(model=Course)
    assert result.total == 1
    assert len(result.items) == 1
    instance = result.items[0]

    assert db.destroy(instance=instance)
    assert db.count(model=Course) == 0


def test_rollback(reset_db):
    """
    GIVEN a db instance
    WHEN calling the rollback method of the db instance
    THEN it should rollback a course instance from being inserted the database
    """
    instance = db.init(model=Course, name=pytest.course_name, created_by=pytest.user_uuid, status='pending')
    db.rollback()
    db.commit()
    assert db.count(model=Course) == 0

    instance = db.init(model=Course, name=pytest.course_name, created_by=pytest.user_uuid, status='pending')
    db.save(instance=instance)
    db.rollback()
    assert db.count(model=Course) == 1


def test_clean_query(reset_db):
    """
    GIVEN a db instance
    WHEN calling the clean_query method of the db instance
    THEN it should return a query
    """
    query = db.clean_query(model=Course)
    assert query is not None


def test_run_query(reset_db, seed_course):
    """
    GIVEN a db instance
    WHEN calling the run_query method of the db instance with a valid query
    THEN it should return the query result
    """
    query = db.clean_query(model=Course)
    course = db.run_query(query=query)
    assert course.total == 1


def test_equal_filter(reset_db, seed_course):
    """
    GIVEN a db instance
    WHEN calling the find method of the db instance with an equal filter
    THEN it should return the query result
    """
    name = pytest.course_name
    course = db.find(model=Course, name=name)
    assert course.total == 1

    course = db.find(model=Course, name=name, uuid=pytest.course.uuid)
    assert course.items[0] == pytest.course


def test_nested_filter(reset_db, seed_course, seed_hole):
    """
    GIVEN a db instance
    WHEN calling the find method of the db instance with a nested filter
    THEN it should return the query result
    """
    course = db.find(model=Course, nested={'hole': {'uuid': pytest.hole.uuid}})
    assert course.total == 1


def test_within_filter():
    """
    GIVEN a db instance
    WHEN calling the find method of the db instance with a within filter
    THEN it should return the query result
    """

    course = db.find(model=Course)
    assert course.total == 1

    course = db.find(model=Course, within={'uuid': [pytest.course.uuid]})
    assert course.total == 1

# def test_has_key_filter():
#     """
#     GIVEN a db instance
#     WHEN calling the find method of the db instance with a has_key filter
#     THEN it should return the query result
#     """
#     
#
#     course = db.find(model=Course)
#     assert course.total == 2
#
#     course = db.find(model=Course, has_key={'uuid': global_course.uuid})
#     assert course.total == 0

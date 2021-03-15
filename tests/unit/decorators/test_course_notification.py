import time

import pytest

from src import services


def test_course_notification_course_created(reset_db, kafka_conn_last_msg):
    pytest.course = services.CourseService().create(status='pending', created_by=pytest.user_uuid,
                                                    name=pytest.course_name)
    time.sleep(0.2)
    msg = kafka_conn_last_msg('courses')
    assert msg.key is not None
    assert msg.key == 'course_created'
    assert msg.value is not None
    assert msg.value['uuid'] == str(pytest.course.uuid)


def test_course_notification_course_approved(kafka_conn_last_msg):
    pytest.course = services.CourseService().update(uuid=pytest.course.uuid, status='active')
    time.sleep(0.2)
    msg = kafka_conn_last_msg('courses')
    assert msg.key is not None
    assert msg.key == 'course_approved'
    assert msg.value is not None
    assert msg.value['uuid'] == str(pytest.course.uuid)

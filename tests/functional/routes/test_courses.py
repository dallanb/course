import json
from datetime import datetime

import pytest

from src import app, services
from src.common import time_now
from tests.helpers import generate_uuid


#############
# SUCCESS
#############

###########
# Create
###########
def test_create_course_w_holes(reset_db):
    """
    GIVEN a Flask application configured for testing
    WHEN the POST endpoint 'courses' is requested
    THEN check that the response is valid
    """
    # Header
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Payload
    payload = {
        'name': pytest.course_name,
        'line_1': pytest.line_1,
        'line_2': pytest.line_2,
        'city': pytest.city,
        'province': pytest.province,
        'country': pytest.country,
        'holes': [{'number': 1, 'par': 3, 'distance': 275}]
    }

    # Request
    response = app.test_client().post('/courses', headers=headers, json=payload)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == 'OK'
    courses = response['data']['courses']
    assert courses['status'] == 'pending'
    assert courses['uuid'] is not None
    assert courses['name'] == pytest.course_name
    assert courses['line_1'] == pytest.line_1
    assert courses['line_2'] == pytest.line_2
    assert courses['city'] == pytest.city
    assert courses['province'] == pytest.province
    assert courses['country'] == pytest.country

    holes = services.HoleService().find()
    assert holes.total == 1


def test_create_course(reset_db):
    """
    GIVEN a Flask application configured for testing
    WHEN the POST endpoint 'courses' is requested
    THEN check that the response is valid
    """
    # Header
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Payload
    payload = {
        'name': pytest.course_name,
        'line_1': pytest.line_1,
        'line_2': pytest.line_2,
        'city': pytest.city,
        'province': pytest.province,
        'country': pytest.country
    }

    # Request
    response = app.test_client().post('/courses', headers=headers, json=payload)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == 'OK'
    courses = response['data']['courses']
    assert courses['status'] == 'pending'
    assert courses['uuid'] is not None
    assert courses['name'] == pytest.course_name
    assert courses['line_1'] == pytest.line_1
    assert courses['line_2'] == pytest.line_2
    assert courses['city'] == pytest.city
    assert courses['province'] == pytest.province
    assert courses['country'] == pytest.country


###########
# Fetch
###########
def test_fetch_course(reset_db, seed_course):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'course' is requested
    THEN check that the response is valid
    """
    course_uuid = pytest.course.uuid

    # Header
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Request
    response = app.test_client().get(f'/courses/{course_uuid}',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == 'OK'
    courses = response['data']['courses']
    assert courses['status'] == 'pending'
    assert courses['uuid'] is not None


###########
# Fetch All
###########
def test_fetch_all_course(reset_db, seed_course):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'courses' is requested
    THEN check that the response is valid
    """
    # Header
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Request
    response = app.test_client().get(f'/courses',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == 'OK'
    assert len(response['data']['courses']) == 1
    courses = response['data']['courses'][0]
    assert courses['status'] == 'pending'
    assert courses['uuid'] is not None


###########
# Update
###########
def test_update_course(reset_db, seed_course):
    """
    GIVEN a Flask application configured for testing
    WHEN the PUT endpoint 'course' is requested
    THEN check that the response is valid
    """
    course_uuid = pytest.course.uuid

    # Header
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Payload
    payload = {
        'status': 'active'
    }

    # Request
    response = app.test_client().put(f'/courses/{course_uuid}',
                                     headers=headers, json=payload)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == 'OK'
    courses = response['data']['courses']
    assert courses['status'] == 'active'
    assert courses['uuid'] is not None


#############
# FAIL
#############


###########
# Create
###########
def test_create_course_fail(reset_db):
    """
    GIVEN a Flask application configured for testing
    WHEN the POST endpoint 'courses' is requested
    THEN check that the response is valid
    """
    # Header
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Payload
    payload = {
        'name': None,
        'line_1': pytest.line_1,
        'line_2': pytest.line_2,
        'city': pytest.city,
        'province': pytest.province,
        'country': pytest.country
    }

    # Request
    response = app.test_client().post('/courses', headers=headers, json=payload)

    # Response
    assert response.status_code == 400


###########
# Update
###########
def test_update_course_fail(reset_db, seed_course):
    """
    GIVEN a Flask application configured for testing
    WHEN the PUT endpoint 'course' is requested
    THEN check that the response is valid
    """
    course_uuid = pytest.course.uuid

    # Header
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}
    # Payload
    payload = {
        'status': 'approved'
    }

    # Request
    response = app.test_client().put(f'/courses/{course_uuid}', headers=headers, json=payload)

    # Response
    assert response.status_code == 500

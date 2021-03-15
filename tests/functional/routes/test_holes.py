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
def test_create_hole(reset_db, seed_course):
    """
    GIVEN a Flask application configured for testing
    WHEN the POST endpoint 'holes' is requested
    THEN check that the response is valid
    """
    course_uuid = pytest.course.uuid
    # Header
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Payload
    payload = {
        'name': pytest.hole_name,
        'number': pytest.hole_number,
        'par': pytest.par,
        'distance': pytest.distance
    }

    # Request
    response = app.test_client().post(f'/courses/{course_uuid}/holes', headers=headers, json=payload)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == 'OK'
    holes = response['data']['holes']
    assert holes['uuid'] is not None
    assert holes['name'] == pytest.hole_name
    assert holes['number'] == pytest.hole_number
    assert holes['par'] == pytest.par
    assert holes['distance'] == pytest.distance


###########
# Fetch
###########
def test_fetch_hole(reset_db, seed_course, seed_hole):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'hole' is requested
    THEN check that the response is valid
    """
    hole_uuid = pytest.hole.uuid

    # Header
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Request
    response = app.test_client().get(f'/holes/{hole_uuid}',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == 'OK'
    holes = response['data']['holes']
    assert holes['uuid'] is not None


###########
# Fetch All
###########
def test_fetch_all_hole(reset_db, seed_course, seed_hole):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'holes' is requested
    THEN check that the response is valid
    """
    # Header
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Request
    response = app.test_client().get(f'/holes',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == 'OK'
    assert len(response['data']['holes']) == 1
    holes = response['data']['holes'][0]
    assert holes['uuid'] is not None


###########
# Update
###########
def test_update_hole(reset_db, seed_course, seed_hole):
    """
    GIVEN a Flask application configured for testing
    WHEN the PUT endpoint 'hole' is requested
    THEN check that the response is valid
    """
    hole_uuid = pytest.hole.uuid

    # Header
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}
    # Payload
    payload = {
        'name': 'Bingo'
    }

    # Request
    response = app.test_client().put(f'/holes/{hole_uuid}',
                                     headers=headers, json=payload)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == 'OK'
    holes = response['data']['holes']
    assert holes['name'] == payload['name']


#############
# FAIL
#############


###########
# Create
###########
def test_create_hole_fail(reset_db, seed_course):
    """
    GIVEN a Flask application configured for testing
    WHEN the POST endpoint 'holes' is requested
    THEN check that the response is valid
    """
    course_uuid = pytest.course.uuid

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
    response = app.test_client().post(f'/courses/{course_uuid}/holes', headers=headers, json=payload)

    # Response
    assert response.status_code == 400


###########
# Update
###########
def test_update_hole(reset_db, seed_course, seed_hole):
    """
    GIVEN a Flask application configured for testing
    WHEN the PUT endpoint 'hole' is requested
    THEN check that the response is valid
    """
    hole_uuid = pytest.hole.uuid

    # Header
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}
    # Payload
    payload = {
        'name': 1
    }

    # Request
    response = app.test_client().put(f'/holes/{hole_uuid}',
                                     headers=headers, json=payload)

    # Response
    assert response.status_code == 400

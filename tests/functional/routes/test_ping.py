from src import app


def test_ping(reset_db):
    response = app.test_client().get('/ping')

    assert response.status_code == 200

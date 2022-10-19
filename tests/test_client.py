#import string
import pytest

def test_home_page_with_fixture(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = client.get("/")
    assert response.status_code == 200

def test_sub_pages(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/static/..' page is requested (GET)
    THEN check that the response is valid
    """
    response = client.get("/static/about.html")
    assert response.status_code == 200

    response = client.get("/static/documentation.html")
    assert response.status_code == 200

    response = client.get("/static/examples.html")
    assert response.status_code == 200
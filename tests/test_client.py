from cgi import test
import string
import pytest
from flask import current_app

Upper = [True, False]
AI_options = ["rejection","mh","gibbs"]

def test_home_page_with_fixture(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/")
    assert response.status_code == 200

def test_sub_pages(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/static/..' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/static/about.html")
    assert response.status_code == 200

    response = test_client.get("/static/documentation.html")
    assert response.status_code == 200

    response = test_client.get("/static/examples.html")
    assert response.status_code == 200


"""
GIVEN data from the form on main_interface
WHEN we want a response back from the server (POST)
THEN check that the response is valid
"""
#################### non mi interessa sapere se i risultati sono corretti,
#################### mi basta sapere che il server sia in grado di rispondere

def test_form_post_EXACT_INFERENCE(test_client):
    with open('esempi/bird_4_cond.lp', 'r') as file:
        program = file.read()
    responde = test_client.post("/", data={
        "inputPr":program,
        "inputQ":"fly",
        "inputEv":"",
        "options":"Exact Inference"
    })
    assert responde.status_code == 200
    
def test_form_post_APPROXIMATE_INFERENCE(test_client):
    with open('esempi/bird_4.lp', 'r') as file:
        program = file.read()
    for opt in AI_options:    
        responde = test_client.post("/", data={
            "inputPr":program,
            "inputQ":"fly(1)",
            "inputEv":"",
            "options":"Approximate Inference",
            "nSamples":"1000",
            "AI_options": opt,
            "Blocks":""        
        })
        assert responde.status_code == 200

 
def test_form_post_MAP_INFERENCE(test_client):
    with open('esempi/gold_map.lp', 'r') as file:
        program = file.read()
    for upper in Upper:
        responde = test_client.post("/", data={
            "inputPr":program,
            "inputQ":"valuable(1)",
            "inputEv":"", #never used
            "options":"Map Inference",
            "Upper": upper
        })
        assert responde.status_code == 200

def test_form_post_ABDUCTION(test_client):
    with open('esempi/bird_4_abd_prob.lp', 'r') as file:
        program = file.read()
    for upper in Upper:
        responde = test_client.post("/", data={
            "inputPr":program,
            "inputQ":"fly(1)",
            "inputEv":"", #never used
            "options":"Abduction",
            "Upper":upper
        })
        assert responde.status_code == 200
    
def test_form_post_PARAMETER_LEARNING(test_client):
    with open('esempi/background_shop.lp', 'r') as file:
        program = file.read()
    for upper in Upper:
        responde = test_client.post("/", data={
            "inputPr":program,
            "inputQ":"none",
            "inputEv":"", #never used
            "options":"Parameter Learning",
            "Upper":upper
        })
        assert responde.status_code == 200
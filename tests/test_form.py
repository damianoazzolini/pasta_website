import pytest
from pasta_website.db import get_db

Upper = [True, False]
AI_options = ["rejection","mh","gibbs"]

"""
GIVEN data from the form on main_interface
WHEN we want a response back from the server (POST)
THEN check that the response is valid and database saved the data
"""
#################### non mi interessa sapere se i risultati sono corretti,
#################### mi basta sapere che il server sia in grado di rispondere

def test_form_post_EXACT_INFERENCE(client, app):
    with open('pasta/examples/conditionals/bird_4_cond.lp', 'r') as file:
        program = file.read()
    responde = client.post("/", data={
        "inputPr":program,
        "inputQ":"fly",
        "inconsistent": False,
        "normalize": False,
        "inputEv":"",
        "options":"Exact Inference"
    })
    assert responde.status_code == 200

    with app.app_context():
        assert get_db().execute(
            "SELECT id_request FROM Request WHERE query = 'fly'",
        ).fetchone() is not None
    
def test_form_post_APPROXIMATE_INFERENCE(client, app):
    with open('pasta/examples/inference/bird_4.lp', 'r') as file:
        program = file.read()
    for opt in AI_options:    
        responde = client.post("/", data={
            "inputPr":program,
            "inputQ":"fly(1)",
            "inconsistent": False,
            "normalize": False,
            "inputEv":"",
            "options":"Approximate Inference",
            "nSamples":"1000",
            "AI_options": opt,
            "Blocks":""        
        })
        assert responde.status_code == 200
    
    with app.app_context():
        assert get_db().execute(
            "SELECT id_request FROM Request WHERE query = 'fly(1)'",
        ).fetchone() is not None

 
def test_form_post_MAP_INFERENCE(client, app):
    with open('pasta/examples/map/gold_map.lp', 'r') as file:
        program = file.read()
    for upper in Upper:
        responde = client.post("/", data={
            "inputPr":program,
            "inputQ":"valuable(1)",
            "inconsistent": False,
            "normalize": False,
            "inputEv":"", #never used
            "options":"Map Inference",
            "Upper": upper
        })
        assert responde.status_code == 200
    
    with app.app_context():
        assert get_db().execute(
            "SELECT id_request FROM Request WHERE query = 'valuable(1)'",
        ).fetchone() is not None

def test_form_post_ABDUCTION(client, app):
    with open('pasta/examples/abduction/bird_4_abd_prob.lp', 'r') as file:
        program = file.read()
    for upper in Upper:
        responde = client.post("/", data={
            "inputPr":program,
            "inputQ":"fly(1)",
            "inconsistent":False,
            "normalize":False,
            "inputEv":"", #never used
            "options":"Abduction",
            "Upper":upper
        })
        assert responde.status_code == 200
    
    with app.app_context():
        assert get_db().execute(
            "SELECT id_request FROM Request WHERE query = 'fly(1)'",
        ).fetchone() is not None
    
def test_form_post_PARAMETER_LEARNING(client, app):
    with open('pasta/examples/learning/background_shop.lp', 'r') as file:
        program = file.read()
    for upper in Upper:
        responde = client.post("/", data={
            "inputPr":program,
            "inputQ":"none",
            #"inconsistent":False,
            #"normalize":False,
            "inputEv":"", #never used
            "options":"Parameter Learning",
            "Upper":upper
        })
        assert responde.status_code == 200

    with app.app_context():
        assert get_db().execute(
            "SELECT id_request FROM Request WHERE option_1 = 'Parameter Learning'",
        ).fetchone() is not None
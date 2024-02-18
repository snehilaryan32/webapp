import pytest
import json
import base64
from flask import json
from app import app  # Import the app from app.py


#############Define Fixtures####################
@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

# Define the test data 
@pytest.fixture
def user_data():
    return {
        "username": "jackson456@gmail.com",
        "password": "testpassword",
        "first_name": "Test",
        "last_name": "User"
    }

@pytest.fixture
def user_data_updated():
    return {
        "password": "newpassword",
        "first_name": "New",
        "last_name": "Name"
    }

# Helper function to create headers for the Authorization
def __create_headers(username, password):
    credentials = base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8')
    return {
        'Authorization': f'Basic {credentials}'
    }

# ##############################################Health Check######################################################
# def test_healthz_endpoint_content(client):
#     # Make a GET request to the /healthz endpoint
#     response = client.get('/healthz')

#     # Check that the response has a status code of 200
#     assert response.status_code == 200

##############################################Test 1 Create and Get User#########################################
def test_create_and_get_user(client, user_data):
    #Create an account using POST call
    response = client.post('/v1/user', data=json.dumps(user_data), content_type='application/json')
    assert response.status_code == 201
    #Using the GET call, validate account exists
    headers = __create_headers(user_data["username"], user_data["password"])
    response = client.get('/v1/user/self', headers=headers)
    assert response.status_code == 200 
    assert response.get_json()["username"] == user_data["username"]

##############################################Test 2 Update and Get User#########################################
def test_update_and_get_user(client, user_data, user_data_updated):
    #Update the account
    response = client.put('/v1/user/self', data = json.dumps(user_data_updated), headers=__create_headers(user_data["username"], user_data["password"]))
    assert response.status_code == 204
    # Using the GET call, validate the account was updated
    response = client.get('/v1/user/self', headers=__create_headers(user_data["username"], user_data_updated["password"]))
    assert response.status_code == 200
    assert response.get_json()["username"] == user_data["username"] #Make sure username is same 
    assert response.get_json()["first_name"] == user_data_updated["first_name"] #Make sure first name is updated
    assert response.get_json()["last_name"] == user_data_updated["last_name"] 
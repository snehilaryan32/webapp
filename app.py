from flask import Flask, make_response, jsonify, request
from flask_httpauth import HTTPBasicAuth
from flask_bcrypt import Bcrypt
from werkzeug.exceptions import BadRequest, MethodNotAllowed
from pydantic import ValidationError    
from models import pydantic_validators
from db_module import db_conn, user_controller


app = Flask(__name__)
auth = HTTPBasicAuth()
bcrypt = Bcrypt()
db_conn.db_bootstrap()


###################################Helper Functions############################################

###Setting Up Header Functions###########
def set_response_headers(response):
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'  
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

###Check for unnecessary Authorization###
def __check_for_unnecessary_auth():
    if 'Authorization' in request.headers:
        raise BadRequest(description="Authorization should not be provided")

###################################Error Handling############################################
@app.errorhandler(BadRequest)
def handle_bad_request(e):
    response = jsonify({"description": "Bad Request"})
    response = set_response_headers(response)
    return response, 400

@app.errorhandler(MethodNotAllowed)
def handle_method_not_allowed(e):
    response = jsonify({})
    response = set_response_headers(response)
    return response, 405

@app.errorhandler(404)
def handle_404(e):
    response = jsonify({})
    response = set_response_headers(response)
    return response, 404

###################################Basic Auth############################################
@auth.verify_password
def verify_password(username, password):
    hash_in_db = user_controller.get_hashed_password(username)
    if hash_in_db and bcrypt.check_password_hash(hash_in_db, password):
        return username


###############################Health Check############################################
@app.route('/healthz', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD'])
def db_health_check():
    response = make_response()
    response.data =  ""
    #Check if the request method is not GET and raise 405
    if request.method != 'GET':
        response.status_code = 405

    else:
        __check_for_unnecessary_auth
        #Check if the request has a payload or URL Parameters were provided and raise 400
        if request.data or request.args:
            response.status_code = 400
        
        #Check if db connection is successful and raise 200
        elif db_conn.db_connect() == True:
            response.status_code = 200

        #Check if db connection is unsuccessful and raise 503
        elif db_conn.db_connect() == False:
            response.status_code = 503

    response = set_response_headers(response)
    return response

###############################User Creation############################################
@app.route('/v1/user', methods=['POST'])
def create_user()
    response = make_response()
    response.headers['Content-Type'] = 'application/json'
    payload = request.get_json(force=True)

    #Check if the request has Authorization and raise BadRequest
    __check_for_unnecessary_auth()
    #Check if all the required fields are provided
    if pydantic_validators.is_valid_payload(payload, pydantic_validators.CreateUserPayload): 
        #Hash the password
        payload["password"] = bcrypt.generate_password_hash(payload['password']).decode('utf-8')
        result = user_controller.create_user(payload)
        if result['status_code'] == 201:
            # Get the User object from db to return attributes in the response
            new_user = user_controller.get_user_details(payload['username'])
            response = jsonify(new_user.get_user_dict())
            response.status_code = result['status_code']
        # To handle all the error cases
        else:
            response = jsonify({"description": result['description']})
            response.status_code = result['status_code']
    else:
        response = jsonify({"description": "Invalid Payload"})
        response.status_code = 400

    response = set_response_headers(response)
    return response 

###############################Get User Details and Post Update#########################################
@app.route('/v1/user/self', methods=['GET', 'PUT'])
@auth.login_required
def get_user():
    response = make_response()
    
    if request.method == 'GET':
        #Check if request has a body or URL Parameters and raise 400
        if request.data or request.args:
            raise BadRequest
        
        else:
            username = auth.current_user()
            user =  user_controller.get_user_details(username)
            # print(user.username)
            if user:
                response.status_code = 200
                response = make_response(jsonify({
                        "id": user.id,
                        "username": user.username, 
                        "first_name": user.first_name, 
                        "last_name": user.last_name, 
                        "account_created": user.account_created, 
                        "account_updated": user.account_updated
                    }),200)
                
    if request.method == 'PUT':
        payload = request.get_json(force=True)
        if pydantic_validators.is_valid_payload(payload, pydantic_validators.UpdateUserPayload):  
            # print("verified")
            payload["password"] = bcrypt.generate_password_hash(payload['password']).decode('utf-8') 
            result = user_controller.update_user_details(auth.current_user(), payload)
            response.status_code = result['status_code']
        else:
            raise BadRequest
    
    response = set_response_headers(response)
    return response


        

    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=8080, debug=True)

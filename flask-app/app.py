from flask import Flask, make_response, jsonify, request
from flask_httpauth import HTTPBasicAuth
from flask_bcrypt import Bcrypt
from werkzeug.exceptions import BadRequest, MethodNotAllowed
from pydantic import ValidationError    
import logging
from pythonjsonlogger import jsonlogger
import os
from models import pydantic_validators
from db_module import db_conn, user_controller
from pubsub_module import publish_msg
from datetime import datetime


db_conn.db_bootstrap()
logging.basicConfig(filename='record.log', level=logging.DEBUG)
app = Flask(__name__)
auth = HTTPBasicAuth()
bcrypt = Bcrypt()

###################################Logging#####################################################
# Set up JSON logging
log_file_path = os.getenv('LOG_FILE_PATH')
logHandler = logging.FileHandler(log_file_path)
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(message)s')
logHandler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(logHandler)
logger.setLevel(logging.DEBUG)
logging.info('App Started')


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
        logging.error('Authorization should not be provided')
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
    logging.error('Resource Not Found')
    return response, 404

@app.errorhandler(401)
def handle_401(e):
    response = jsonify({"message": "Unauthorized: Invalid username or password"})
    response = set_response_headers(response)
    logging.error('Unauthorized: Invalid username or password')
    return response, 401

@app.errorhandler(500)
def handle_500(e):
    response = jsonify({"message": "Wrong Username or Password"})
    response = set_response_headers(response)
    logging.error('Wrong Username or Password')
    return response, 500, 404

###################################Basic Auth############################################
@auth.verify_password
def verify_password(username, password):
    hash_in_db = user_controller.get_hashed_password(username)
    if hash_in_db and bcrypt.check_password_hash(hash_in_db, password):
        return username
    else:
        return False
###############################Health Check############################################
@app.route('/healthz', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD'])
def db_health_check():
    logging.info('Health Check')
    response = make_response()
    response.data =  ""
    #Check if the request method is not GET and raise 405
    if request.method != 'GET':
        response.status_code = 405
        logging.error('Wrong Method Used for Health Check')

    else:
        __check_for_unnecessary_auth()
        conn = db_conn.db_connect()
        #Check if the request has a payload or URL Parameters were provided and raise 400
        if request.data or request.args:
            response.status_code = 400
            logging.error('Payload or URL Parameters Provided for Health Check')
        
        #Check if db connection is successful and raise 200
        elif conn == True:
            response.status_code = 200
            db_conn.db_close(conn)
            logging.info('Health Check Successful')

        #Check if db connection is unsuccessful and raise 503
        elif conn == False:
            response.status_code = 503
            logging.error('Health Check Failed')

    response = set_response_headers(response)
    return response

###############################User Creation############################################
@app.route('/v1/user', methods=['POST']) 
def create_user():
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
            new_user = user_controller.get_user_details(payload['username']).get_user_dict()
            response = jsonify(new_user)
            response.status_code = result['status_code']
            # data_to_pub = {"first_name": new_user.first_name, "last_name": new_user.last_name, "username": new_user.username, "token_id": str(new_user.id)} 
            data_to_pub = publish_msg.generate_message_dict(new_user)
            if os.getenv('ENVIRONMENT') == 'production':
                publish_msg.publish_message(data_to_pub) #Publish the user details to Pub/Sub
            logging.info('User Created')
        # To handle all the error cases
        else:
            response = jsonify({"description": result['description']})
            response.status_code = result['status_code']
            logging.error(result['description'])    
    else:
        response = jsonify({"description": "Invalid Payload"})
        response.status_code = 400
        logging.error('Invalid Payload For User Creation')

    response = set_response_headers(response)
    return response 

###############################Verify User Email Id#####################################################
@app.route('/verify-email/<token_uuid>', methods=['GET'])
def verify_email(token_uuid):
    response = make_response()
    expire_time = user_controller.get_email_tracker_details(token_uuid)
    print(expire_time)
    # expire_time = datetime(*expire_time)
    # print(expire_time)
    if datetime.now() > expire_time[0]:
        response = jsonify({"message": "The link has expired."})
        response.status_code = 400
        logging.warning('Link Expired')
    else:
        result = user_controller.verify_user(token_uuid)
        if result["status_code"] == 200:
            response = jsonify({"message": "Email verified successfully."})
            response.status_code = 200
            logging.info('Email Verified')
        else:
            response = jsonify({"message": "An error occurred during verification."})
            response.status_code = 500
            logging.warning('Error Occurred During Email Verification')
    return response

###############################Get User Details and Post Update#########################################
@app.route('/v1/user/self', methods=['GET', 'PUT'])
@auth.login_required
def get_user():
    response = make_response()
    
    if request.method == 'GET':
        #Check if request has a body or URL Parameters and raise 400
        if request.data or request.args:
            logging.error('Payload or URL Parameters Provided for User Details')
            raise BadRequest
        
        else:
            username = auth.current_user()
            user =  user_controller.get_user_details(username)
            # print(user.username)
            if user:
                if user.verified == True:
                    response.status_code = 200
                    response = make_response(jsonify({
                            "id": user.id,
                            "username": user.username, 
                            "first_name": user.first_name, 
                            "last_name": user.last_name, 
                            "account_created": user.account_created, 
                            "account_updated": user.account_updated
                        }),200)
                    logging.info('User Details Fetched')
                else:
                    response = make_response(jsonify({"message":"Email not verified"}), 403)
                    logging.warning('Email Not Verified for User Details')
            # else:
            #     respose = make_response(jsonify({"message":"wrong username"}), 401)
                
    if request.method == 'PUT':
        payload = request.get_json(force=True)
        if pydantic_validators.is_valid_payload(payload, pydantic_validators.UpdateUserPayload):  
            user = user_controller.get_user_details(auth.current_user())
            if user.verified == True:  
                payload["password"] = bcrypt.generate_password_hash(payload['password']).decode('utf-8') 
                result = user_controller.update_user_details(auth.current_user(), payload)
                response.status_code = result['status_code']
                logging.info('User Details Updated')
            else:
                response = make_response(jsonify({"message":"Email not verified"}), 403)
                logging.warning('Email Not Verified for User Update')
        else:
            logging.error('Invalid Payload for User Update')
            raise BadRequest
    
    response = set_response_headers(response)
    return response



    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=8080, debug=True)
from flask import Flask, make_response, jsonify, request
from db_module import db_conn, user_controller
from flask_httpauth import HTTPBasicAuth
from flask_bcrypt import Bcrypt

app = Flask(__name__)
auth = HTTPBasicAuth()
bcrypt = Bcrypt()

db_conn.db_bootstrap()

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
        #Check if the request has a payload or URL Parameters were provided and raise 400
        if request.data or request.args:
            response.status_code = 400
        
        #Check if db connection is successful and raise 200
        elif db_conn.db_connect() == True:
            response.status_code = 200

        #Check if db connection is unsuccessful and raise 503
        elif db_conn.db_connect() == False:
            response.status_code = 503

    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'  
    response.headers['X-Content-Type-Options'] = 'nosniff'

    return response


###############################User Creation############################################
@app.route('/user', methods=['POST'])
def create_user():
    response = make_response()
    payload = request.get_json(force=True)
    #Check if all the required fields are provided
    if "email" not in payload.keys() or "first_name" not in payload.keys() or "last_name" not in payload.keys() or "password" not in payload.keys():
        response = jsonify({"message": "Bad Request Please provide all required fields"})
        response.status_code = 400
    else:
        result = user_controller.create_user(payload['email'], payload['first_name'], payload['last_name'], bcrypt.generate_password_hash(payload['password']).decode('utf-8'))
        response = jsonify({"message": result['message']})
        response.status_code = result['status_code']
    return response


###############################Get User Details#########################################
@app.route('/user/self', methods=['GET'])
@auth.login_required
def get_user():
    response = make_response()
    username = auth.current_user()
    user =  user_controller.get_user_details(username)
    print(user.username)
    if user:
        response.status_code = 200
        print(user.username, type(user.first_name), user.last_name)
        response = make_response(jsonify({
                "id": user.id,
                "username": user.username, 
                "first_name": user.first_name, 
                "last_name": user.last_name, 
                "account_created": user.account_created, 
                "account_updated": user.account_updated
            }),200)
        return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
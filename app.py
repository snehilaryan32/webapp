from flask import Flask, make_response, jsonify, request
from db_module import db_conn, user_controller
app = Flask(__name__)

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



@app.route('/user', methods=['POST'])
def create_user():
    response = make_response()
    payload = request.get_json(force=True)
    #Check if all the required fields are provided
    if "email" not in payload.keys() or "first_name" not in payload.keys() or "last_name" not in payload.keys() or "password" not in payload.keys():
        response.status_code = 400
        response.data = "Bad Request Please provide all required fields"
    else:
        result = user_controller.create_user(payload['email'], payload['first_name'], payload['last_name'], payload['password'])
        print(result)
        response.status_code = result['status_code']
        response.data = result['message']
    return response
















#     return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
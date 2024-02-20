#!/bin/bash
unzip flask-app.zip
cd flask-app
# Set Up Python Environment after scp the new requirements 
python3 -m venv myenv
source myenv/bin/activate
export DB_HOST="localhost"
export DB_PORT=5432
export DB_NAME=$DB_NAME
export DB_USER=$DB_USER
export DB_PASSWORD=$DB_PASS
pip3 install --upgrade pip
pip3 install -r requirements.txt
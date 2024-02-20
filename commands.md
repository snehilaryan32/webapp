# Commands 

## Setting Up the environment
# Python 
python3 -m venv myenv
source myenv/bin/activate
pip3 install -r requirements.txt

flask run -p 8080

# code to test modules 
python -m db_module.user_controller

## Database
### Start The Service 
sudo service postgresql start
sudo service postgresql status
sudo service postgresql stop
# set the 
sudo -u postgres psql

#Connect to db
\c database_name

#Create User
sudo -u postgres createuser snehilaryan 
alter user snehilaryan with encrypted password 'your_pass';

## Add extension for uuid
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

## Alter table to add id column
ALTER TABLE users ADD COLUMN id UUID PRIMARY KEY DEFAULT uuid_generate_v4();

# Django
django-admin startproject app
django-admin startapp healthapp

# Killing processes to free up port
sudo kill -9 $(sudo lsof -t -i :8080)

# unzip the codebase 
unzip Snehil_Aryan_002767640_01.zip -d demo

# Gcloud commands 
gcloud services enable sourcerepo.googleapis.com
gcloud services enable compute.googleapis.com
gcloud services enable servicemanagement.googleapis.com
gcloud services enable storage-api.googleapis.com

#List the services enabled
gcloud services list --enabled

#Zip the package
zip -r packer_image/flask-app.zip flask-app/
gcloud compute images delete flask-app

# Systemctl

sudo cp packer_image/flaskapp.service /etc/systemd/system/flaskapp.service
sudo systemctl status flaskapp
sudo systemctl stop flaskapp
journalctl -u flaskapp
curl -v '127.0.0.1:8080/healthz'
sudo setenforce 0
sudo systemctl daemon-reload

curl -v --request POST 'http://127.0.0.1:8080/v1/user' \
--header 'Content-Type: application/json' \
--data-raw ' {
    "username": "new_user@gmail.com",
    "password": "secure_password",
    "first_name": "New",
    "last_name": "User"
}'
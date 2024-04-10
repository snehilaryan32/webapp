# Commands 

## Setting Up the environment
# Python 
python3 -m venv myenv
source myenv/bin/activate
pip3 install -r flask-app/requirements.txt

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
gcloud compute images delete flask-app-new

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
    "username": "new_user.com",
    "password": "secure_password",
    "first_name": "New",
    "last_name": "User"
}'

packer build -var 'image_name=flask-app' ./flask_image.pkr.hcl

gcloud projects add-iam-policy-binding csye6225-414117 --member="serviceAccount:svc-packer@csye6225-414117.iam.gserviceaccount.com" --role="roles/secretmanager.admin"

gcloud secrets versions access latest --secret="db-private-ip"



gcloud compute instance-templates create INSTANCE_TEMPLATE_NAME \
  --machine-type=e2-small \
  --boot-disk-size=20 \
  --boot-disk-type=pd-balanced \
  --image=flask-app-new \
  --subnet=webapp \
  --network-tier=app-vpc-assignment7 \
  --tags=webapp \
  --metadata=startup-script="#! /bin/bash
    touch /home/packer/flaskapp.env
    echo 'DB_HOST=${local.db_host}' >> /home/packer/flaskapp.env
    echo 'DB_PORT=5432' >> ${local.env_file_path}
    echo 'DB_NAME=${var.db_name}' >> /home/packer/flaskapp.env
    echo 'DB_USER=${var.db_user}' >> /home/packer/flaskapp.env
    echo 'DB_PASSWORD=${random_password.password.result}' >> /home/packer/flaskapp.env
    echo 'LOG_FILE_PATH=${var.log_file_path}' >> /home/packer/flaskapp.env
    echo 'PROJECT_ID=${var.project_id}' >> /home/packer/flaskapp.env
    echo 'PUBSUB_TOPIC_ID=${var.pubsub_topic_name}' >> /home/packer/flaskapp.env
    echo 'ENVIRONMENT=${var.app_env}' >> /home/packer/flaskapp.env
    sudo chown csye6225:csye6225 /home/packer/flaskapp.env
    sudo chmod 644 /home/packer/flaskapp.env
    sudo systemctl daemon-reload
    sudo systemctl restart flaskapp"
  --service-account=google_service_account.service_account.email
  --scopes=var.scopes \
  --region=us-central1-a \
  --project=var.project_id

  /home/packer/flaskapp.env

gcloud compute instance-templates create test-from-terminal \
  --project=csye6225-414117 \
  --region=us-central1\
  --machine-type=e2-small \
  --boot-disk-size=20 \
  --boot-disk-type=pd-balanced \
  --image=flask-app-image-20240409035435 \
  --network=app-vpc-assignment8 \
  --subnet=webapp \
  --tags=webapp \
  --scopes=https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/logging.admin,https://www.googleapis.com/auth/pubsub \
  --service-account=service-account-webapp-id@csye6225-414117.iam.gserviceaccount.com 

gcloud projects add-iam-policy-binding csye6225-414117 \
    --member serviceAccount:svc-packer@csye6225-414117.iam.gserviceaccount.com \
    --role roles/compute.instanceAdmin.v1

gcloud projects add-iam-policy-binding csye6225-414117 \
    --member serviceAccount:svc-packer@csye6225-414117.iam.gserviceaccount.com \
    --role roles/compute.instanceAdmin.v1

gcloud compute networks subnets add-iam-policy-binding webapp \
    --region=us-central1 \
    --project=csye6225-414117 \
    --member=serviceAccount:svc-packer@csye6225-414117.iam.gserviceaccount.com \
    --role=roles/compute.networkUser

gcloud projects add-iam-policy-binding csye6225-414117 \
    --member=serviceAccount:svc-packer@csye6225-414117.iam.gserviceaccount.com \
    --role=roles/compute.loadBalancerAdmin

gcloud compute instance-groups managed rolling-action start-update webapp-instance-manager \
    --version=template=test-from-actions-metadata \
    --region=us-central1 \


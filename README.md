# SSH into the server
ssh root@162.243.160.168

# SCP
scp webapp-main.zip root@162.243.160.168:/root/cloud-app

# Postgres Set Up
# Install postgres
sudo yum install postgresql-server postgresql-contrib
sudo postgresql-setup initdb

sudo service postgresql start
sudo service postgresql status
sudo service postgresql stop



## Create DB
CREATE DATABASE firstdb;

## Create User set password and grant permissions
CREATE USER aryan WITH PASSWORD ;
GRANT ALL PRIVILEGES ON DATABASE firstdb TO aryan;

# Python Setup
sudo yum update
sudo yum install python3

<!-- sudo yum install python3-pip -->

# Unzip the files in wsl
sudo yum install unzip
unzip webapp-main

sudo kill -9 $(sudo lsof -t -i :8080)


## Pytest 
python3 -m pytest -p no:warnings
# Running the application
python3 -m venv myenv
source myenv/bin/activate
export DB_HOST="localhost"
export DB_PORT=5432
export DB_NAME="firstdb"



#!/bin/bash
# Install Python, unzip, postgres
sudo yum install -y unzip
sudo yum install -y python3
sudo yum install -y python3-pip
# sudo yum install python3-devel
# Install Postgres and devel package to solve pg_config error
sudo yum install -y postgresql-server postgresql-contrib postgresql-devel
sudo postgresql-setup initdb

# Postgres Setup. Change directorty to 
cd /tmp 
sudo service postgresql start
sudo -u postgres psql -c "CREATE DATABASE $DB_NAME;"
sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';"
sudo -u postgres psql -c "ALTER USER $DB_USER WITH SUPERUSER;"
cd /home/packer
# Unzip the package
unzip flask-app.zip
cd flask-app
cat requirements.txt
# Set Up Python Environment after scp the new requirements 
python3 -m venv myenv
source myenv/bin/activate
pip3 install --upgrade pip
# pip3 install wheel
# pip3 install psycopg2
pip3 install -r requirements.txt
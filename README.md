# Commands 

## Setting Up the environment
# Python 
python3 -m venv myenv
source myenv/bin/activate
pip3 install -r requirements.txt
source environment.sh

flask run -p 8089

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

# Django
django-admin startproject app
django-admin startapp healthapp

# Killing processes to free up port
sudo kill -9 $(sudo lsof -t -i :8080)

# unzip the codebase 
unzip Snehil_Aryan_002767640_01.zip -d demo
#!/bin/bash
unzip flask-app.zip
cd flask-app
# Set Up Python Environment after scp the new requirements 
python3 -m venv myenv
source myenv/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt
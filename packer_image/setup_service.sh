#!/bin/bash
# Move the service file, update selinux policy for the file, reload systemd manager configuration, and enable the service, create a svcuser
sudo mv /home/packer/flaskapp.service /etc/systemd/system/flaskapp.service
sudo groupadd csye6225
sudo useradd -r -g csye6225 -s /usr/sbin/nologin csye6225
sudo chown csye6225:csye6225 /home/packer/flask-app
sudo chown csye6225:csye6225 /home/packer/flask-app/myenv
sudo chown csye6225 /home/packer/flask-app/myenv/bin/gunicorn
echo "SELINUX=permissive" | sudo tee /etc/selinux/config
sudo systemctl daemon-reload
sudo setenforce 0
sudo systemctl enable flaskapp
sudo systemctl start flaskapp
sudo systemctl status flaskapp

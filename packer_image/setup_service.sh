#!/bin/bash
# Move the service file, update selinux policy for the file, reload systemd manager configuration, and enable the service, create a svcuser
sudo mv /home/packer/flaskapp.service /etc/systemd/system/flaskapp.service
sudo chown -R csye6225:csye6225 /home/packer/flask-app # Change the ownership of the directory to the user in svc file
sudo adduser csye6225 --system --shell /usr/sbin/nologin
echo "SELINUX=permissive" | sudo tee /etc/selinux/config
sudo systemctl daemon-l start flaskappreload
sudo setenforce 0
sudo systemctl enable flaskapp
sudo systemct
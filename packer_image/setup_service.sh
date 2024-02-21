#!/bin/bash
# Move the service file, update selinux policy for the file, reload systemd manager configuration, and enable the service, create a svcuser
sudo mv /home/packer/flaskapp.service /etc/systemd/system/flaskapp.service
sudo adduser csye6225 --system --shell /usr/sbin/nologin
# sudo chown csye6225:csye6225 /etc/systemd/system/flaskapp.service
sudo chown csye6225 /home/packer/flask-app/myenv/bin/gunicorn

echo "SELINUX=permissive" | sudo tee /etc/selinux/config
sudo systemctl daemon-reload
sudo setenforce 0
sudo systemctl enable flaskapp
sudo systemctl restart flaskapp
#!/bin/bash
# Move the service file, update selinux policy for the file, reload systemd manager configuration, and enable the service
sudo mv /home/packer/flaskapp.service /etc/systemd/system/flaskapp.service
echo "SELINUX=permissive" | sudo tee /etc/selinux/config
sudo systemctl daemon-reload
setenforce 0
sudo systemctl enable flaskapp
sudo systemctl start flaskapp
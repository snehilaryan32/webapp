#!/bin/bash
# Move the service file, update selinux policy for the file, reload systemd manager configuration, and enable the service
sudo mv /home/packer/flaskapp.service /etc/systemd/system/flaskapp.service
sudo setenforce 0
sudo systemctl daemon-reload
sudo systemctl enable flaskapp
sudo systemctl start flaskapp
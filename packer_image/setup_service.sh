#!/bin/bash
# Move the service file, reload systemd manager configuration, and enable the service
sudo mv /home/packer/flaskapp.service /etc/systemd/system/
sudo setenforce 0
sudo systemctl daemon-reload
ls -l /etc/systemd/system/
sudo systemctl enable flaskapp
sudo systemctl start flaskapp
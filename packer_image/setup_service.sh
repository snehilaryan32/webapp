#!/bin/bash
# Move the service file, update selinux policy for the file, reload systemd manager configuration, and enable the service, create a svcuser
sudo mv /home/packer/flaskapp.service /etc/systemd/system/flaskapp.service
sudo groupadd csye6225
sudo useradd -r -g csye6225 -s /usr/sbin/nologin csye6225
sudo chown -R csye6225:csye6225 /home/packer/flask-app
sudo chmod -R 755 /home/packer/flask-app
sudo chown csye6225:csye6225 /home/packer/flask-app/myenv/bin/gunicorn
sudo chmod 755 /home/packer/flask-app/myenv/bin/gunicorn
sudo chown csye6225:csye6225 /home/packer
sudo chmod 700 /home/packer

################Setup Logging####################################
sudo mkdir /var/log/my-app
sudo chown csye6225:csye6225 /var/log/my-app
sudo mv /home/packer/config.yaml /etc/google-cloud-ops-agent/config.yaml
sudo systemctl restart google-cloud-ops-agent

###############Serup flaskapp service############################
echo "SELINUX=permissive" | sudo tee /etc/selinux/config
sudo systemctl daemon-reload
sudo setenforce 0
sudo systemctl enable flaskapp
sudo systemctl start flaskapp
# sudo systemctl status flaskapp

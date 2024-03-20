#!/bin/bash
# Install Python, unzip, postgres, google ops agent
# sudo yum update -y
sudo yum install -y unzip
sudo yum install -y python3
sudo yum install -y python3-pip
curl -sSO https://dl.google.com/cloudagents/add-google-cloud-ops-agent-repo.sh
sudo bash add-google-cloud-ops-agent-repo.sh --also-install




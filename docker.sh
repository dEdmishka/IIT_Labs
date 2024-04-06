#!/bin/bash

sudo apt-get update -y
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ubuntu
sudo su -
docker pull dockermachine321/labiit:latest
docker run -d -p 80:80 dockermachine321/labiit
docker run -d --name watchtower --restart=always -v /var/run/docker.sock:/var/run/docker.sock containrrr/watchtower --interval 60

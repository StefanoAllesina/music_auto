#!/bin/bash
sudo yum groupinstall -y "Development Tools"
sudo yum install -y ImageMagick python36 python36-devel
sudo pip-3.6 install pipenv
curl --silent --location https://rpm.nodesource.com/setup_8.x | sudo bash -
sudo yum -y install nodejs
git clone https://github.com/StefanoAllesina/music_auto.git -b release-1.0.0
cd $PWD/GUICode/html
sudo pipenv install
npm install
sudo nohup PORT=80 npm start &
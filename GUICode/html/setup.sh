#!/bin/bash
sudo yum groupinstall "Development Tools"
sudo yum install ImageMagick python36 python36-devel
sudo pip-3.6 install pipenv
git clone https://github.com/StefanoAllesina/music_auto.git -b release-1.0.0
cd $PWD/GUICode/html
pipenv install
npm install
sudo nohup npm start
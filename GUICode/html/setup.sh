#!/bin/bash
yum groupinstall -y "Development Tools"
yum install -y ImageMagick python36 python36-devel
pip-3.6 install pipenv
curl --silent --location https://rpm.nodesource.com/setup_8.x | sudo bash -
yum -y install nodejs
git clone https://github.com/StefanoAllesina/music_auto.git -b release-1.0.0
cd $PWD/music_auto/GUICode/html
export PATH="$PATH:/usr/local/bin"
pipenv install
npm install
export PORT=80
nohup npm start &
touch /var/swap.img
chmod 600 /var/swap.img
dd if=/dev/zero of=/var/swap.img bs=1024k count=10000
mkswap /var/swap.img
swapon /var/swap.img
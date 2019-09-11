#!/bin/sh

# Installing Python 3.6 and pip
apt-get update --fix-missing
apt-get install -y software-properties-common
add-apt-repository ppa:jonathonf/python-3.6
apt-get update --fix-missing
apt-get install -y build-essential python3.6 python3.6-dev
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py --force-reinstall
apt-get install -y python3-tk


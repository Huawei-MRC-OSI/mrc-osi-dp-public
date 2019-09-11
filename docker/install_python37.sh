#!/bin/sh

# Installing Python 3.7 and pip
apt-get update --fix-missing && \
apt-get install -y software-properties-common && \
add-apt-repository ppa:deadsnakes/ppa && \
apt-get update --fix-missing && \
apt-get install -y python3.7 python3.7-distutils && \
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1 && \
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
python3 get-pip.py --force-reinstall


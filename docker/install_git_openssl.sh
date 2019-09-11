#!/bin/bash
mkdir /tmp/git-build
cd /tmp/git-build
sudo sed -i "s/^# deb-src/deb-src/" /etc/apt/sources.list
sudo apt-get update --fix-missing
sudo apt-get install -y build-essential fakeroot dpkg-dev liberror-perl git-man
apt-get source git
sudo apt-get build-dep -y git
sudo apt-get install -y libcurl4-openssl-dev
dpkg-source -x git_*
cd git*/
sed -i "s/gnutls/openssl/g" ./debian/control
sed -i "/TEST *= *test/d" ./debian/rules
sudo dpkg-buildpackage -rfakeroot -b
cd ..
sudo dpkg -i git_*.deb

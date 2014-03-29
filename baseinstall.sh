#!/bin/bash
# run as root
# installer script for Clio dependancies

# install git
apt-get install git-core

# install mysql
apt-get install mysql-server

# install python modules
apt-get install python-dev
apt-get install python-setuptools
apt-get install python-pip
pip install scipy
pip install numpy
pip install pandas
pip install mysqldb

# install postfix smtp server
# apt-get install postfix

# install ftp server
# apt-get install vsftpd

# Execute sql script to build MySQL database
mysql -u root -p < build_database.sql



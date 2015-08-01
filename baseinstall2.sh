#!/bin/bash
# run as root
# installer script for Clio dependancies

# install git
# apt-get install git-core

# install mysql
apt-get install mysql-server
# apt-get install mysqldump

# install python modules
apt-get install python-dev
apt-get install python-setuptools
apt-get install python-pip
apt-get install python-scipy, python-numpy, python-pandas, python-mysqldb, ipython, python-lxml

pip install scikit-learn
pip install requests
pip install "ipython[notebook]"
pip install matplotlib

# install postfix smtp server
# apt-get install postfix

# install ftp server
# apt-get install vsftpd

# Execute sql script to build MySQL database
# mysql -u root -p < build_database.sql



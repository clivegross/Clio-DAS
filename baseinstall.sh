#!/bin/bash
# installer script for required tools and python
# modules for Clio to run

# install git
sudo apt-get install git-core

# install mysql
sudo apt-get install mysql-server

# install python modules
sudo apt-get install python-dev
sudo apt-get install python-setuptools
sudo apt-get install python-pip
sudo apt-get install python-numpy
sudo apt-get install python-scipy
sudo apt-get install python-pandas
sudo apt-get install python-mysqldb
sudo apt-get install ipython-notebook

# install postfix smtp server
sudo apt-get install postfix

# install ftp server
sudo apt-get install vsftpd

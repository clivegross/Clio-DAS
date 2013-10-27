Clio-DAS
========

Debian based ASX market data acquisition system to store in a MySQL database
-----------------------------------

Instructions for building *Clio-DAS*:

1.	Install Raspbian Wheezy on Raspberry Pi
2.	Set up static eth0 NIC
3.	Clone this repo to root of default user directory
4.	Install the required packages and python modules via baseinstall.sh:

		sudo sh baseinstall.sh

5.	Execute in MySQL build_database.sql to create database Clio, set permissions etc
6.	Edit my.cnf file to allow remote connections by commenting out the following line:

		bind-address=YOUR-SERVER-IP

6.	Setup FTP login. Edit vsftpd.conf, ie:

		sudo vi /etc/vsftpd.conf

to allow ftp connections, search through the file and make the following changes-
Set:

		anonymous_enable=NO

Uncomment the follwoing lines:

		local_enable=YES
		write_enable=YES

Add to end of file:

		force_dot_files=YES

Restart the FTP server with:

		sudo service vsftpd restart'

7. Import companies into the Company table from csv using csv2companytable.py:

		python csv2companytable.py companylist.csv



Clio-DAS
========

Debian based ASX market data acquisition system to store in a MySQL database
-----------------------------------

Instructions for building *Clio-DAS*:

1.	Install Raspbian Wheezy on Raspberry Pi
2.	Set up static eth0 NIC
3.	Clone this repo to root of default user directory
4.	Execute 'sudo sh baseinstall.sh' to install required packages and python modules
5.	Execute build_database.sql to create MySQL database Clio, set permissions etc
6.	Setup FTP login. Edit vsftpd.conf (sudo vi /etc/vsftpd.conf) to allow ftp connections, search through the file and make the following changes-
Set: anonymous_enable=NO
Uncomment: local_enable=YES
Uncomment: write_enable=YES
Add to end of file: force_dot_files=YES
Restart the FTP server with 'sudo service vsftpd restart'
7. Import companies into the Company table from csv using csv2companytable.py


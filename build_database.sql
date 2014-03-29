/* List of tables
Company
id int
symbol varchar(5)
name varchar(40)
industryid int
still_exists bool

Announcement
id int
companyid int
publish_time timestamp
is_price_sensitive bool
headline varchar(100)

Industry
id int
name varchar(40)

Price
id int
companyid int
timestamp_UTC timestamp
open decimal
close decimal
high decimal
low decimal
volume int
*/

# create user clio
CREATE USER 'clio'@'localhost' IDENTIFIED BY 'password';

# create database clio
CREATE DATABASE clio;

# grant user clio@localhost access to database clio
GRANT ALL PRIVILEGES ON clio.* To 'clio'@'localhost' IDENTIFIED BY 'password';
# grant user clio@[remote] access to database clio
GRANT ALL PRIVILEGES ON clio.* TO 'clio'@'%' IDENTIFIED BY 'password' WITH GRANT OPTION;

USE clio

# create tables
CREATE TABLE Company(id INT NOT NULL AUTO_INCREMENT,
					symbol VARCHAR(10) NOT NULL,
					name VARCHAR(50),
					industryid INT,
					still_exists BOOL,
					PRIMARY KEY (id));

CREATE TABLE Announcement(id INT NOT NULL AUTO_INCREMENT,
						companyid INT NOT NULL,
						publish_time TIMESTAMP NOT NULL,
						is_price_sensitive BOOL NOT NULL,
						headline VARCHAR(100) NOT NULL,
						PRIMARY KEY (id));

CREATE TABLE Price(id INT NOT NULL AUTO_INCREMENT,
					companyid INT NOT NULL,
					timestamp_UTC TIMESTAMP NOT NULL,
					open DECIMAL NOT NULL,
					close DECIMAL NOT NULL,
					high DECIMAL NOT NULL,
					low DECIMAL NOT NULL,
					volume INT NOT NULL,
					PRIMARY KEY (id));

CREATE TABLE Industry(id INT NOT NULL AUTO_INCREMENT,
					name VARCHAR(40),
					PRIMARY KEY (id));

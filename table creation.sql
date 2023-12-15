
CREATE DATABASE cybercafe;
USE cybercafe;
CREATE TABLE customers
	(   cus_id  	smallint    PRIMARY KEY AUTO_INCREMENT,
		name		char(30)    NOT NULL,
        password	char(30)	NOT NULL); 
CREATE TABLE bookings
	(	cus_id		smallint	REFERENCES customers(cus_id),
		service_id	smallint	REFERENCES rate(service_id),
		date 		date		NOT NULL,
        time		time		NOT NULL ,
        qty			smallint);
CREATE TABLE rate
	(	service_id	smallint	PRIMARY KEY,
		service		char(50)	NOT NULL,
        rate		int			NOT NULL );
CREATE TABLE transaction
	(	trans_id	smallint    PRIMARY KEY AUTO_INCREMENT,
		cus_id		smallint	REFERENCES customers(cus_id),
		service_id	smallint	REFERENCES rate(service_id) ON UPDATE CASCADE,
        qty			smallint	NOT NULL,
        date		date		DEFAULT NULL);

        

INSERT INTO rate
VALUES	
		(1,'black and white printout',5),
		(2,'colour printout',10),
        (3,'advance booking(1 hour)',60),
        (4,'net surfing (per hour)',70),
        (5,"gaming computer",130),
        (6,'play station 3',100),
        (7,'play station 4',120),
        (8,'play station 5',150),
        (9,'XBOX 360',110),
        (10,'XBOX ONE',130),
        (11,'XBOX SERIES X',140); 
		

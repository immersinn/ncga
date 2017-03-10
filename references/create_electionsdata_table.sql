# Create elections_data table for ncga database
# http://dev.mysql.com/doc/refman/5.7/en/create-table.html

DROP TABLE IF EXISTS elections_data;
#@ _CREATE_TABLE_
CREATE TABLE elections_data
(
	id			INT NOT NULL AUTO_INCREMENT,
	district	INT NOT NULL,
	session		VARCHAR(20) NOT NULL,
	chamber		CHAR(1) NOT NULL,
	name		VARCHAR(50) NOT NULL,
	party		VARCHAR(20) NOT NULL,
	incombant	BOOL, 
	won			BOOL NOT NULL,
	votes		INT,
	PRIMARY KEY (id)
) ENGINE = InnoDB;
#@ _CREATE_TABLE_


DROP TABLE IF EXISTS erl;
#@ _CREATE_TABLE_
CREATE TABLE erl
(
	id				INT NOT NULL AUTO_INCREMENT,
	election_id		INT NOT NULL,
	repr_table		VARCHAR(30) NOT NULL,
	FOREIGN KEY (election_id) REFERENCES elections_data (id),

) ENGINE = InnoDB;
#@ _CREATE_TABLE_

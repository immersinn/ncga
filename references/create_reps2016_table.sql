# Create reps2016 table for ncga database
# http://dev.mysql.com/doc/refman/5.7/en/create-table.html

DROP TABLE IF EXISTS reps2016;
#@ _CREATE_TABLE_
CREATE TABLE reps2016
(
	id			INT NOT NULL AUTO_INCREMENT,
	name		VARCHAR(50) NOT NULL,
	chamber		CHAR(1) NOT NULL,
	party		VARCHAR(20) NOT NULL,
	PRIMARY KEY (id),
	CONSTRAINT uni_name UNIQUE (name)

) ENGINE = InnoDB;
#@ _CREATE_TABLE_

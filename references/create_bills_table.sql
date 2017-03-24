# Create bills table for ncga database
# http://dev.mysql.com/doc/refman/5.7/en/create-table.html

DROP TABLE IF EXISTS bills;
#@ _CREATE_TABLE_
CREATE TABLE bills
(
	id			INT NOT NULL AUTO_INCREMENT,
	bill_id 	VARCHAR(8) NOT NULL,
	session		YEAR NOT NULL,
	date_filed	DATE NOT NULL,
	title		VARCHAR(250),
	link		VARCHAR(150) NOT NULL,
	PRIMARY KEY (id),
	INDEX yid (session)
) ENGINE = InnoDB;
#@ _CREATE_TABLE_

ALTER TABLE bills ADD CONSTRAINT billyear UNIQUE (bill_id, session);

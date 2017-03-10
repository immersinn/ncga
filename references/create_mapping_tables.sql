# Create mapping tables table for ncga database
# http://dev.mysql.com/doc/refman/5.7/en/create-table.html


DROP TABLE IF EXISTS master_reprs;
#@ _CREATE_TABLE_
CREATE TABLE master_reprs
(
	id					INT NOT NULL AUTO_INCREMENT,
	sponsor_id			INT NOT NULL,
	sponsor_session		VARCHAR(20) NOT NULL,
	PRIMARY KEY (id)
) ENGINE = InnoDB;
#@ _CREATE_TABLE_


DROP TABLE IF EXISTS brl;
#@ _CREATE_TABLE_
CREATE TABLE brl
(
	id				INT NOT NULL AUTO_INCREMENT,
	bill_id			INT NOT NULL,
	sponsor_id		INT NOT NULL,
	sponsor_type	VARCHAR(50),
	FOREIGN KEY (bill_id) REFERENCES bills (id),
	FOREIGN KEY (sponsor_id) REFERENCES master_reprs (id),

) ENGINE = InnoDB;
#@ _CREATE_TABLE_

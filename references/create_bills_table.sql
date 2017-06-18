# Create bills table for ncga database
# http://dev.mysql.com/doc/refman/5.7/en/create-table.html

DROP TABLE IF EXISTS bills;
#@ _CREATE_TABLE_
CREATE TABLE bills
(
    id				INT NOT NULL AUTO_INCREMENT,
	bill_id 		VARCHAR(8) NOT NULL,
	edition      VARCHAR(20) NOT NULL,
	link			VARCHAR(150) NOT NULL,
	page_scraped	TINYINT(1) NOT NULL DEFAULT 0,
	PRIMARY KEY (id),
    FOREIGN KEY (bill_id) REFERENCES bills (id),
) ENGINE = InnoDB;
#@ _CREATE_TABLE_

ALTER TABLE bills ADD CONSTRAINT billed UNIQUE (bill_id, edition);
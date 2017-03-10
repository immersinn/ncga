# Create reps2014 table for ncga database
# http://dev.mysql.com/doc/refman/5.7/en/create-table.html

DROP TABLE IF EXISTS reps2014;

CREATE TABLE reps2014 (
	id INT NOT NULL AUTO_INCRIMENT,
	PRIMARY KEY (id),
	eid, name, chamber, party)
ENGINE=MyISAM
SELECT id AS eid, name, chamber, party
FROM elections_data
WHERE won == 'True' AND session == '2014';


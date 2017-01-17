
-- Schema for the Game IDs table
CREATE TABLE bill_links (
	session 		TEXT,
    house 		TEXT,
	bill 		INT,
    label       TEXT,
	html 		TEXT, 
	pdf 		TEXT,
);
CREATE INDEX ncgalinks_house ON bill_links(house);
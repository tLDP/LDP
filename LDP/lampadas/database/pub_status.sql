DROP TABLE pub_status;

CREATE TABLE pub_status
(
	pub_status		CHAR		NOT NULL,
	pub_status_name		TEXT,
	pub_status_desc		TEXT,
	
	PRIMARY KEY (pub_status)
);

GRANT SELECT ON pub_status TO "www-data";
GRANT SELECT ON pub_status TO root;

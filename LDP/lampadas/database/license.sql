DROP TABLE license;

CREATE TABLE license
(
	license		CHAR(12)	NOT NULL,
	free		BOOLEAN		NOT NULL,

	PRIMARY KEY (license)
);

CREATE TABLE license
(
	license_code	CHAR(12)	NOT NULL,
	free		BOOLEAN		NOT NULL	DEFAULT False,
	dfsg_free	BOOLEAN		NOT NULL	DEFAULT False,
	osi_cert_free	BOOLEAN		NOT NULL	DEFAULT False,
	url		TEXT,
	sort_order	INT4		NOT NULL,

	PRIMARY KEY (license_code)
);

CREATE TABLE pub_status
(
	pub_status_code		CHAR		NOT NULL,
	sort_order		INT4		NOT NULL,
	created			TIMESTAMP	NOT NULL DEFAULT now(),
	updated			TIMESTAMP	NOT NULL DEFAULT now(),
	
	PRIMARY KEY (pub_status_code)
);

CREATE INDEX pub_status_upd_idx ON pub_status (updated);
CREATE INDEX pub_status_ctd_idx ON pub_status (created);

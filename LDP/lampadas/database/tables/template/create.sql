CREATE TABLE template
(
	template_code		CHAR(12)	NOT NULL,
	template		TEXT		NOT NULL,
	created			TIMESTAMP	NOT NULL	DEFAULT now(),
	updated			TIMESTAMP	NOT NULL	DEFAULT now(),

	PRIMARY KEY (template_code)
);

CREATE INDEX template_upd_idx ON template (updated);
CREATE INDEX template_ctd_idx ON template (created);

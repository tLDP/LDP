CREATE TABLE error_i18n
(
	err_id			INT4		NOT NULL,
	lang			CHAR(2)		NOT NULL,
	err_name		TEXT		NOT NULL,
	err_desc		TEXT,

	PRIMARY KEY (err_id, lang)
);

CREATE TABLE news_i18n
(
	news_id		INT4	NOT NULL	REFERENCES news(news_id),
	lang		CHAR(2)	NOT NULL	REFERENCES language(lang_code),
	news		TEXT	NOT NULL,

	PRIMARY KEY (news_id, lang)
);

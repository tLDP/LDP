DELETE FROM page_i18n;
DELETE FROM page;

INSERT INTO page (page_code, template_code) VALUES ('test',	'default');
INSERT INTO page (page_code, template_code) VALUES ('about',	'default');

INSERT INTO page_i18n (page_code, lang, page) VALUES ('test',	'EN', 'Test Page');
INSERT INTO page_i18n (page_code, lang, page) VALUES ('about',	'EN', 'This page is about Lampadas.');


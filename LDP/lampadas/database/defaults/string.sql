DELETE FROM string_i18n;
DELETE FROM string;

INSERT INTO string(string_code) VALUES ('test');
INSERT INTO string(string_code) VALUES ('header');
INSERT INTO string(string_code) VALUES ('footer');

INSERT INTO string_i18n(string_code, lang, string) VALUES ('test',	'EN', 'Test Text');
INSERT INTO string_i18n(string_code, lang, string) VALUES ('header',	'EN', '<h1><center>Lampadas Header</center></h1>');
INSERT INTO string_i18n(string_code, lang, string) VALUES ('footer',	'EN', '<h1><center>Lampadas Footer</center></h1>');

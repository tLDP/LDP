DELETE FROM string_i18n;
DELETE FROM string;

INSERT INTO string(string_id) VALUES (1);
INSERT INTO string(string_id) VALUES (2);
INSERT INTO string(string_id) VALUES (3);

INSERT INTO string(string_id) VALUES (1000);
INSERT INTO string(string_id) VALUES (2000);

INSERT INTO string_i18n(string_id, lang, string) VALUES (1, 'EN', 'Test Text');
INSERT INTO string_i18n(string_id, lang, string) VALUES (2, 'EN', '<h1><center>Lampadas Header</center></h1>');
INSERT INTO string_i18n(string_id, lang, string) VALUES (3, 'EN', '<h1><center>Lampadas Footer</center></h1>');

INSERT INTO string_i18n(string_id, lang, string) VALUES (1000, 'EN', '|header| |body| |footer|');
INSERT INTO string_i18n(string_id, lang, string) VALUES (2000, 'EN', 'Hi, this page will be about Lampadas.');

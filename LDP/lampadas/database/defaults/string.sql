DELETE FROM string_i18n;
DELETE FROM string;

INSERT INTO string(string_code) VALUES ('test');
INSERT INTO string(string_code) VALUES ('project');
INSERT INTO string(string_code) VALUES ('projectshort');
INSERT INTO string(string_code) VALUES ('mmtitle');
INSERT INTO string(string_code) VALUES ('home');
INSERT INTO string(string_code) VALUES ('doctable');
INSERT INTO string(string_code) VALUES ('docdetails');

INSERT INTO string_i18n(string_code, lang, string) VALUES ('test',		'EN', 'Test Text');
INSERT INTO string_i18n(string_code, lang, string) VALUES ('test',		'FR', 'Texte de Test');

INSERT INTO string_i18n(string_code, lang, string) VALUES ('footer',		'EN', '<h1><center>Lampadas Footer</center></h1>');
INSERT INTO string_i18n(string_code, lang, string) VALUES ('footer',		'FR', '<h1><center>Pied de page Lampadas</center></h1>');

INSERT INTO string_i18n(string_code, lang, string) VALUES ('project',		'EN', 'The Linux Documentation Project');
INSERT INTO string_i18n(string_code, lang, string) VALUES ('project',		'FR', 'Le Linux Documentation Project');

INSERT INTO string_i18n(string_code, lang, string) VALUES ('projectshort',	'EN', 'The LDP');
INSERT INTO string_i18n(string_code, lang, string) VALUES ('projectshort',	'FR', 'Le LDP');

INSERT INTO string_i18n(string_code, lang, string) VALUES ('mmtitle',		'EN', 'Main Menu');
INSERT INTO string_i18n(string_code, lang, string) VALUES ('mmtitle',		'FR', 'Menu Principal');

INSERT INTO string_i18n(string_code, lang, string) VALUES ('home',		'EN', 'Home');
INSERT INTO string_i18n(string_code, lang, string) VALUES ('home',		'FR', 'Racine');

INSERT INTO string_i18n(string_code, lang, string) VALUES ('doctable',		'EN', 'DocTable');
INSERT INTO string_i18n(string_code, lang, string) VALUES ('doctable',		'FR', 'Table des documents');

INSERT INTO string_i18n(string_code, lang, string) VALUES ('docdetails',	'EN', 'Document Details');
INSERT INTO string_i18n(string_code, lang, string) VALUES ('docdetails',	'FR', 'D&eacute;tails du Document');

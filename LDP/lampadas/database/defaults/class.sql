DELETE FROM class_i18n;
DELETE FROM class;

INSERT INTO class (class_id) VALUES (1);
INSERT INTO class (class_id) VALUES (2);
INSERT INTO class (class_id) VALUES (3);
INSERT INTO class (class_id) VALUES (4);
INSERT INTO class (class_id) VALUES (5);
INSERT INTO class (class_id) VALUES (6);
INSERT INTO class (class_id) VALUES (7);

INSERT INTO class_i18n (class_id, lang, clsss_name, class_description) VALUES (1, 'EN', 'HOWTO',	'A HOWTO describes how to do something on Linux.');
INSERT INTO class_i18n (class_id, lang, clsss_name, class_description) VALUES (1, 'FR', 'HOWTO',	'Un HOWTO documente cas pratique.');

INSERT INTO class_i18n (class_id, lang, clsss_name, class_description) VALUES (2, 'EN', 'Mini',		'A small HOWTO.');
INSERT INTO class_i18n (class_id, lang, clsss_name, class_description) VALUES (2, 'FR', 'Mini',	'Un mini HOWTO.');

INSERT INTO class_i18n (class_id, lang, clsss_name, class_description) VALUES (3, 'EN', 'FAQ',		'A list of Frequently Asked Questions.');
INSERT INTO class_i18n (class_id, lang, clsss_name, class_description) VALUES (3, 'FR', 'FAQ',	'Une Foire Aux Questions.');

INSERT INTO class_i18n (class_id, lang, clsss_name, class_description) VALUES (4, 'EN', 'Template',	'A template for writing your own document.');
INSERT INTO class_i18n (class_id, lang, clsss_name, class_description) VALUES (4, 'FR', 'Modèle',	'Un modèle pour &eacute;crire vos documents.');

INSERT INTO class_i18n (class_id, lang, clsss_name, class_description) VALUES (5, 'EN', 'QuickRef',	'One-page and other short references.');
INSERT INTO class_i18n (class_id, lang, clsss_name, class_description) VALUES (5, 'FR', 'Fiche',	'Une fiche de r&eacute;f&eacute;rence rapide.');

INSERT INTO class_i18n (class_id, lang, clsss_name, class_description) VALUES (6, 'EN', 'Guide',	'A Guide is a full-length book.');
INSERT INTO class_i18n (class_id, lang, clsss_name, class_description) VALUES (6, 'FR', 'Guide',	'Une Guide est un livre qui couvre largement un sujet.');

INSERT INTO class_i18n (class_id, lang, clsss_name, class_description) VALUES (7, 'EN', 'Intro',	'A document containing background or introductory information, suitable for a novice.');
INSERT INTO class_i18n (class_id, lang, clsss_name, class_description) VALUES (7, 'FR', 'Intro',	'Un document d''introduction convient particuli&egrave;rement bien aux d&eacute;butants.');

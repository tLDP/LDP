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
INSERT INTO class_i18n (class_id, lang, clsss_name, class_description) VALUES (1, 'FR', 'Le HOWTO',	'Un HOWTO describes how to do something on Linux.');
INSERT INTO class_i18n (class_id, lang, clsss_name, class_description) VALUES (2, 'EN', 'Mini',		'A small HOWTO.');
INSERT INTO class_i18n (class_id, lang, clsss_name, class_description) VALUES (2, 'FR', 'Le Mini',	'Un small HOWTO.');
INSERT INTO class_i18n (class_id, lang, clsss_name, class_description) VALUES (3, 'EN', 'FAQ',		'A list of Frequently Asked Questions.');
INSERT INTO class_i18n (class_id, lang, clsss_name, class_description) VALUES (3, 'FR', 'Le FAQ',	'Un list of Frequently Asked Questions.');
INSERT INTO class_i18n (class_id, lang, clsss_name, class_description) VALUES (4, 'EN', 'Template',	'A template for writing your own document.');
INSERT INTO class_i18n (class_id, lang, clsss_name, class_description) VALUES (4, 'FR', 'Le Template',	'Un template for writing your own document.');
INSERT INTO class_i18n (class_id, lang, clsss_name, class_description) VALUES (5, 'EN', 'QuickRef',	'One-page and other short references.');
INSERT INTO class_i18n (class_id, lang, clsss_name, class_description) VALUES (5, 'FR', 'Le QuickRef',	'Un One-page and other short references.');
INSERT INTO class_i18n (class_id, lang, clsss_name, class_description) VALUES (6, 'EN', 'Guide',	'A Guide is a full-length book.');
INSERT INTO class_i18n (class_id, lang, clsss_name, class_description) VALUES (6, 'FR', 'Le Guide',	'Un Guide is a full-length book.');
INSERT INTO class_i18n (class_id, lang, clsss_name, class_description) VALUES (7, 'EN', 'Intro',	'A document containing background or introductory information, suitable for a novice.');
INSERT INTO class_i18n (class_id, lang, clsss_name, class_description) VALUES (7, 'FR', 'Le Intro',	'Un document containing background or introductory information, suitable for a novice.');

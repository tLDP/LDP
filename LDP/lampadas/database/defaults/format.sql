DELETE FROM format_i18n;
DELETE FROM format;

INSERT INTO format (format_id) VALUES (1);
INSERT INTO format (format_id) VALUES (2);
INSERT INTO format (format_id) VALUES (3);
INSERT INTO format (format_id) VALUES (4);
INSERT INTO format (format_id) VALUES (5);
INSERT INTO format (format_id) VALUES (6);

INSERT INTO format_i18n (format_id, lang, format_name, format_desc) VALUES (1, 'EN', 'SGML',	'Standard Generalized Markup Language');
INSERT INTO format_i18n (format_id, lang, format_name, format_desc) VALUES (1, 'FR', 'SGML',	'Standard Generalized Markup Language');

INSERT INTO format_i18n (format_id, lang, format_name, format_desc) VALUES (2, 'EN', 'PDF',	'Portable Document Format');
INSERT INTO format_i18n (format_id, lang, format_name, format_desc) VALUES (2, 'FR', 'PDF',	'Portable Document Format');

INSERT INTO format_i18n (format_id, lang, format_name, format_desc) VALUES (3, 'EN', 'Text',	'Plain Text');
INSERT INTO format_i18n (format_id, lang, format_name, format_desc) VALUES (3, 'FR', 'Text',	'Texte pur');

INSERT INTO format_i18n (format_id, lang, format_name, format_desc) VALUES (4, 'EN', 'XML',	'eXtensible Markup Language');
INSERT INTO format_i18n (format_id, lang, format_name, format_desc) VALUES (4, 'FR', 'XML',	'eXtensible Markup Language');

INSERT INTO format_i18n (format_id, lang, format_name, format_desc) VALUES (5, 'EN', 'LaTeX',	'LaTeX');
INSERT INTO format_i18n (format_id, lang, format_name, format_desc) VALUES (5, 'FR', 'LaTeX',	'LaTeX');

INSERT INTO format_i18n (format_id, lang, format_name, format_desc) VALUES (6, 'EN', 'Wiki',	'WikiText');
INSERT INTO format_i18n (format_id, lang, format_name, format_desc) VALUES (6, 'FR', 'Wiki',	'WikiText');


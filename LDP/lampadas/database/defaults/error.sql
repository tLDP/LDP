DELETE FROM error_i18n;
DELETE FROM error;

INSERT INTO error (err_id) VALUES (1);
INSERT INTO error (err_id) VALUES (2);

INSERT INTO error_i18n (err_id, lang, err_name, err_desc) VALUES (1, 'EN', 'File not found',	'The source file does not exist in the Lampadas cvs cache.');
INSERT INTO error_i18n (err_id, lang, err_name, err_desc) VALUES (1, 'FR', 'Fichier introuvable',	'Ce fichier n''existe pas dans le cache du cvs de Lampadas.');

INSERT INTO error_i18n (err_id, lang, err_name, err_desc) VALUES (2, 'EN', 'File not writable',	'The source file exists, but is not writable.');
INSERT INTO error_i18n (err_id, lang, err_name, err_desc) VALUES (2, 'FR', 'Fichier prot&eacute;g&eacute; en &eacute;criture',	'Ce fichier existe, mais est prot&eacute;g&eacute; en &eacute;criture.');


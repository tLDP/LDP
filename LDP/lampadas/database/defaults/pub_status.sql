DELETE FROM pub_status;

INSERT INTO pub_status (pub_status) VALUES ('R');
INSERT INTO pub_status (pub_status) VALUES ('O');
INSERT INTO pub_status (pub_status) VALUES ('P');
INSERT INTO pub_status (pub_status) VALUES ('W');
INSERT INTO pub_status (pub_status) VALUES ('?');
INSERT INTO pub_status (pub_status) VALUES ('D');
INSERT INTO pub_status (pub_status) VALUES ('A');
INSERT INTO pub_status (pub_status) VALUES ('N');
INSERT INTO pub_status (pub_status) VALUES ('C');

INSERT INTO pub_status_i18n (pub_status, lang, pub_status_name, pub_status_desc) VALUES ('R', 'EN', 'Replaced',		'Replaced by another document.');
INSERT INTO pub_status_i18n (pub_status, lang, pub_status_name, pub_status_desc) VALUES ('R', 'FR', 'Remplac&eacute;',		'Remplac&eacute; par un autre document.');

INSERT INTO pub_status_i18n (pub_status, lang, pub_status_name, pub_status_desc) VALUES ('O', 'EN', 'Offsite',		'Available at another site.');
INSERT INTO pub_status_i18n (pub_status, lang, pub_status_name, pub_status_desc) VALUES ('O', 'FR', 'Hors site',		'Disponible sur un autre site.');

INSERT INTO pub_status_i18n (pub_status, lang, pub_status_name, pub_status_desc) VALUES ('P', 'EN', 'Pending',		'A work in progress, which is not yet available.');
INSERT INTO pub_status_i18n (pub_status, lang, pub_status_name, pub_status_desc) VALUES ('P', 'FR', 'En cours',		'Travail en cours qui n''est pas encore disponible.');

INSERT INTO pub_status_i18n (pub_status, lang, pub_status_name, pub_status_desc) VALUES ('W', 'EN', 'Wishlist',		'A document that has been proposed but not yet written.');
INSERT INTO pub_status_i18n (pub_status, lang, pub_status_name, pub_status_desc) VALUES ('W', 'FR', 'Souhait',		'Ce document a &eacute;t&eacute; demand&eacute; ou propos&eacute;, mais n''a pas encore &eacute;t&eacute; &eacute;crit.');

INSERT INTO pub_status_i18n (pub_status, lang, pub_status_name, pub_status_desc) VALUES ('?', 'EN', 'Unknown',		'Unknown');
INSERT INTO pub_status_i18n (pub_status, lang, pub_status_name, pub_status_desc) VALUES ('?', 'FR', 'Inconnu',		'Inconnu');

INSERT INTO pub_status_i18n (pub_status, lang, pub_status_name, pub_status_desc) VALUES ('D', 'EN', 'Deleted',		'Deleted');
INSERT INTO pub_status_i18n (pub_status, lang, pub_status_name, pub_status_desc) VALUES ('D', 'FR', 'Effac&eacute;',		'Effac&eacute;');

INSERT INTO pub_status_i18n (pub_status, lang, pub_status_name, pub_status_desc) VALUES ('A', 'EN', 'Archived',		'Currently available from the LDP, but only as an archive.');
INSERT INTO pub_status_i18n (pub_status, lang, pub_status_name, pub_status_desc) VALUES ('A', 'FR', 'Archiv&eacute;',		'Actuellement disponible, mais au titre d''archive.');

INSERT INTO pub_status_i18n (pub_status, lang, pub_status_name, pub_status_desc) VALUES ('N', 'EN', 'Active',		'Currently available from the LDP.');
INSERT INTO pub_status_i18n (pub_status, lang, pub_status_name, pub_status_desc) VALUES ('N', 'FR', 'Actif',		'Actuellement disponible.');

INSERT INTO pub_status_i18n (pub_status, lang, pub_status_name, pub_status_desc) VALUES ('C', 'EN', 'Cancelled',	'Development was cancelled before publication.');
INSERT INTO pub_status_i18n (pub_status, lang, pub_status_name, pub_status_desc) VALUES ('C', 'FR', 'Annul&eacute;',	'R&eacute;daction interrompue avant publication.');


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
INSERT INTO pub_status_i18n (pub_status, lang, pub_status_name, pub_status_desc) VALUES ('O', 'EN', 'Offsite',		'Available at another site.');
INSERT INTO pub_status_i18n (pub_status, lang, pub_status_name, pub_status_desc) VALUES ('P', 'EN', 'Pending',		'A work in progress, which is not yet available.');
INSERT INTO pub_status_i18n (pub_status, lang, pub_status_name, pub_status_desc) VALUES ('W', 'EN', 'Wishlist',		'A document that has been proposed but not yet written.');
INSERT INTO pub_status_i18n (pub_status, lang, pub_status_name, pub_status_desc) VALUES ('?', 'EN', 'Unknown',		'Unknown');
INSERT INTO pub_status_i18n (pub_status, lang, pub_status_name, pub_status_desc) VALUES ('D', 'EN', 'Deleted',		'Deleted');
INSERT INTO pub_status_i18n (pub_status, lang, pub_status_name, pub_status_desc) VALUES ('A', 'EN', 'Archived',		'Currently available from the LDP, but only as an archive.');
INSERT INTO pub_status_i18n (pub_status, lang, pub_status_name, pub_status_desc) VALUES ('N', 'EN', 'Active',		'Currently available from the LDP.');
INSERT INTO pub_status_i18n (pub_status, lang, pub_status_name, pub_status_desc) VALUES ('C', 'EN', 'Cancelled',	'Development was cancelled before publication.');


DELETE FROM review_status_i18n;
DELETE FROM review_status;

INSERT INTO review_status (review_status) VALUES ('U');
INSERT INTO review_status (review_status) VALUES ('P');
INSERT INTO review_status (review_status) VALUES ('R');
INSERT INTO review_status (review_status) VALUES ('N');

INSERT INTO review_status_i18n (review_status, lang, review_status_name, review_status_desc) VALUES ('U', 'EN', 'Unreviewed',	'This document has not yet been reviewed.');
INSERT INTO review_status_i18n (review_status, lang, review_status_name, review_status_desc) VALUES ('U', 'FR', 'FUnreviewed',	'F:This document has not yet been reviewed.');
INSERT INTO review_status_i18n (review_status, lang, review_status_name, review_status_desc) VALUES ('P', 'EN', 'Pending',	'A review is currently in progress.');
INSERT INTO review_status_i18n (review_status, lang, review_status_name, review_status_desc) VALUES ('P', 'FR', 'FPending',	'F:A review is currently in progress.');
INSERT INTO review_status_i18n (review_status, lang, review_status_name, review_status_desc) VALUES ('R', 'EN', 'Reviewed',	'A review has been completed.');
INSERT INTO review_status_i18n (review_status, lang, review_status_name, review_status_desc) VALUES ('R', 'FR', 'FReviewed',	'F:A review has been completed.');
INSERT INTO review_status_i18n (review_status, lang, review_status_name, review_status_desc) VALUES ('N', 'EN', 'Needed',	'A review is needed, but has not yet been performed.');
INSERT INTO review_status_i18n (review_status, lang, review_status_name, review_status_desc) VALUES ('N', 'FR', 'FNeeded',	'F:A review is needed, but has not yet been performed.');

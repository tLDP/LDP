DELETE FROM section_i18n;
DELETE FROM section;

INSERT INTO section (section_code) VALUES ('main');
INSERT INTO section (section_code) VALUES ('misc');

INSERT INTO section_i18n (section_code, lang, section_name) VALUES ('main', 'EN', 'Main Menu');
INSERT INTO section_i18n (section_code, lang, section_name) VALUES ('main', 'FR', 'Menu Principal');

INSERT INTO section_i18n (section_code, lang, section_name) VALUES ('misc', 'EN', 'Misc Menu');
INSERT INTO section_i18n (section_code, lang, section_name) VALUES ('misc', 'FR', 'Menu Divers');

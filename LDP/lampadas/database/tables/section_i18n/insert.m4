m4_changequote([, ])m4_dnl
m4_define(insert,m4_dnl
[INSERT INTO section_i18n(section_code, lang, section_name)
VALUES ('$1', 'I18N_lang_code', '$2');])m4_dnl

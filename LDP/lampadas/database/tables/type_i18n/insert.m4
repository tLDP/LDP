m4_changequote([, ])m4_dnl
m4_define(insert,m4_dnl
[INSERT INTO type_i18n(type_code, lang, type_name, type_desc)
VALUES ('$1', 'I18N_lang_code', '$2', '$3');])m4_dnl

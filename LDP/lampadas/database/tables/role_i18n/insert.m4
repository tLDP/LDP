m4_changequote([, ])m4_dnl
m4_define(insert, [INSERT INTO role_i18n(role, lang, role_name, role_desc)
VALUES ('$1', 'I18N_lang_code', '$2', '$3');])m4_dnl

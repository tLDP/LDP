m4_changequote([, ])m4_dnl
m4_define(insert, [INSERT INTO audience_i18n(audience_code, lang, audience_name, audience_desc)
VALUES ('$1', 'I18N_Lang_Code', '$2', '$3');])m4_dnl

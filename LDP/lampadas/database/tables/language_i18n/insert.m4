m4_changequote([, ])m4_dnl
m4_define(insert, [INSERT INTO language_i18n(isocode, lang, language_name)
VALUES ('$1', 'I18N_lang_code', '$2');])m4_dnl

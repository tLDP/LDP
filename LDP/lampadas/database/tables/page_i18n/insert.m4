m4_changequote([, ])m4_dnl
m4_define(insert, [INSERT INTO page_i18n(page_code, lang, title, page)
VALUES ('$1', 'I18N_lang_code', '$2', '$3');])m4_dnl

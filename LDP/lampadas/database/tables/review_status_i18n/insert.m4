m4_define(insert,m4_dnl
[INSERT INTO review_status_i18n(review_status, lang, review_status_name, review_status_desc)
VALUES ('$1', 'I18N_lang_code', '$2', '$3');])m4_dnl

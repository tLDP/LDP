m4_changequote([, ])m4_dnl
m4_define(insert, [INSERT INTO topic_i18n(topic_code, lang, topic_name, topic_desc)
VALUES ('$1', 'I18N_lang_code', '$2', '$3');])m4_dnl

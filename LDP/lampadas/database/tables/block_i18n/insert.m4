m4_changequote([, ])m4_dnl
m4_define(insert, [INSERT INTO block_i18n(block_code, lang, block)
VALUES ('$1', 'I18N_lang_code', '$2');])m4_dnl

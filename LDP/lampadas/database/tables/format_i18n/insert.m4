m4_changequote([, ])m4_dnl
m4_define(insert, [INSERT INTO format_i18n(format_id, lang, format_name, format_desc)
VALUES ($1, 'I18N_lang_code', '$2', '$3' );])m4_dnl

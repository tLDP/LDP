m4_define(insert,m4_dnl
[INSERT INTO collection_i18n(collection_code, lang, collection_name, collection_desc)
VALUES ('$1', 'I18N_lang_code', '$2', '$3');])m4_dnl

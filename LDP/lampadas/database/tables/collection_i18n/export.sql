SELECT collection_code, lang, collection_name, collection_desc
FROM collection_i18n
WHERE lang = :I18N_lang_code
ORDER BY collection_code;


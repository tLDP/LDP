SELECT type_code, lang, type_name, type_desc
FROM type_i18n
WHERE lang = :I18N_lang_code
ORDER BY type_code;


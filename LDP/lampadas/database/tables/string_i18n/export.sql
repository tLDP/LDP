SELECT string_code, lang, string
FROM string_i18n
WHERE lang = :I18N_lang_code
ORDER BY string_code;

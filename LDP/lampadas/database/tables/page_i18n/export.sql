SELECT page_code, lang, title, menu_name, page, version
FROM page_i18n
WHERE lang = :I18N_lang_code
ORDER BY page_code;

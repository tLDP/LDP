m4_define(insert,[m4_dnl
INSERT INTO string_i18n(string_code, lang, string)
VALUES (m4_dnl
string_or_null($1), m4_dnl
'I18N_lang_code', m4_dnl
string_or_null($2)[]m4_dnl
);])m4_dnl

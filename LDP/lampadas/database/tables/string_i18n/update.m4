m4_changequote([, ])m4_dnl
m4_define(insert, [UPDATE string_i18n SET string='$2' 
WHERE string_code='$1' AND lang='I18N_lang_code';])m4_dnl


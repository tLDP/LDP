m4_changequote([, ])m4_dnl
m4_define(string_or_null,
[m4_ifelse(m4_len([$1]), 0, [null], ['$1'])])m4_dnl

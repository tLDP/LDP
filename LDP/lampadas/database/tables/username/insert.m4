m4_changequote([, ])m4_dnl
m4_define(insert, [INSERT INTO username(user_id, username, session_id,
	first_name, middle_name, surname, email, admin, sysadmin,
	password, notes, stylesheet)
VALUES ($1, '$2', '$3',
	'$4', '$5', '$6', '$7', '$8', '$9',
	'$10', '$11', '$12');])m4_dnl

m4_dnl      username, first_name, middle_name, surname, 
m4_dnl      email, admin, sysadmin, password, notes, stylesheet

insert(admin, Site, [], Administrator,
	[], t, f, password,
	[This is the Site Administrator account.
	Please change the password before your Lampadas server goes live!],
)

insert(sysadmin, System, [], Administrator,
	[], t, t, password,
	[This is the System Administrator account.
	Please change the password before your Lampadas server goes live!],
)


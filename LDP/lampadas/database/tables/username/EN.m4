m4_dnl      username, first_name, middle_name, surname, 
mr_dnl      email, admin, sysadmin, password, notes, stylesheet

insert(admin, Site, [], Administrator,
	[], t, f, password,
	[This is the Site Administrator account.
	Please change the password before your Lampadas server goes live!],
	[default])

insert(sysadmin, System, [], Administrator,
	[], t, t, password,
	[This is the System Administrator account.
	Please change the password before your Lampadas server goes live!],
	[default])

insert(english, John, [Q.], User,
	[], f, f, password,
	[This is a test English account. It should be deleted before release!],
	[ldp])

insert(david, David, [C.], Merrill,
    [david@lupercalia.net], t, t, [byteme], [Lampadas lead developer.], [ldp])

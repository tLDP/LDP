insert(admin, Site, [], Administrator,
	[], t, f, password,
	[This is the Site Administrator account.
	Please change the password before your Lampadas server goes live!],
	[default])

insert(sysadmin, Site, [], Administrator,
	[], t, t, password,
	[This is the System Administrator account.
	Please change the password before your Lampadas server goes live!],
	[default])

insert(user, John, [Q.], User,
	[], f, f, password,
	[This is a test account. It should be deleted before release!],
	[default])

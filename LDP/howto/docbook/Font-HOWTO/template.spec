Name: myfonts
Summary: Collection of My Funny Fonts
Version: 1.0
Release: 1
License: GPL
Group: User Interface/X
Source: %{name}.tar.gz
BuildRoot: %{_tmppath}/build-root-%{name}
BuildArch: noarch
Requires: freetype
Packager: Avi Alkalay <avi@unix.sh>
Prefix: /usr/share/fonts
Url: http://myfonts.com/

%description
These are the fonts used in our marketing campaign, designed by our marketing agency specially for us.
The package includes the following fonts: Bodoni, Bodoni Black, Company Logo, Outline Company Logo, etc.


%prep

%setup -q -n %{name}

%build

%install
mkdir -p $RPM_BUILD_ROOT/%{prefix}
cp -r %{name}/ $RPM_BUILD_ROOT/%{prefix}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,0755)
%{prefix}/%{name}


%post
{
	ttmkfdir -d %{prefix}/%{name} \
		-o %{prefix}/%{name}/fonts.scale
	umask 133
	/usr/X11R6/bin/mkfontdir %{prefix}/%{name}
	/usr/sbin/chkfontpath -q -a %{prefix}/%{name}
	[ -x /usr/bin/fc-cache ] && /usr/bin/fc-cache
} &> /dev/null || :


%preun
{
	if [ "$1" = "0" ]; then
		cd %{prefix}/%{name}
		rm -f fonts.dir fonts.scale fonts.cache*
	fi
} &> /dev/null || :

%postun
if [ "$1" = "0" ]; then
  /usr/sbin/chkfontpath -q -r %{prefix}/%{name}
fi
[ -x /usr/bin/fc-cache ] && /usr/bin/fc-cache



%changelog
* Thu Dec 14 2002 Avi Alkalay <avi@unix.sh> 1.0
- Tested
- Ready for deployment
* Thu Dec 10 2002 Avi Alkalay <avi@unix.sh> 0.9
- First version of the template

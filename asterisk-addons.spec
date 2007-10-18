%define version 1.4.4
%define release %mkrel 1

Summary:	Additional addons for Asterisk
Name:		asterisk-addons
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Servers
URL:		http://www.asterisk.org/
Source:		ftp://ftp.digium.com/pub/asterisk/%{name}-%{version}.tar.bz2
Patch0:		asterisk-addons-1.4.0-mdk.diff
Patch1:		asterisk-addons-1.2.0-20051030-ooh323c_avoid_version.diff
Patch2:		asterisk-addons-1.2.1-bristuff-0.3.0-PRE-1l.diff
BuildRequires:	MySQL-devel
BuildRequires:	asterisk-devel >= 1.2.0
BuildRequires:	automake1.7
Requires:	asterisk
Buildroot:	%{_tmppath}/%{name}-%{version}

%description
Asterisk is a complete PBX in software. It runs on Linux and
provides all of the features you would expect from a PBX and more.
Asterisk does voice over IP in three protocols, and can
interoperate with almost all standards-based telephony equipment
using relatively inexpensive hardware. This package contains
additional addons for asterisk.

%prep

%setup -q
%patch0 -p1
#patch1 -p0
#patch2 -p0

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;
		
for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

# lib64 fix
find . -type f | xargs perl -pi -e "s|/usr/lib|%{_libdir}|g"

%build
%configure
%make
#	CFLAGS="%{optflags} -pipe -Wall -fPIC -DPIC -D_REENTRANT -D_GNU_SOURCE -I%{_includedir}/mysql"

#pushd asterisk-ooh323c
#export WANT_AUTOCONF_2_5=1
#rm -f configure
#libtoolize --copy --force && aclocal-1.7 && autoheader && automake-1.7 --add-missing && autoconf
#%configure2_5x
#%make CFLAGS="%{optflags} -pipe -Wall -fPIC -DPIC -DGNU -D_GNU_SOURCE -D_REENTRANT -D_COMPACT"
#popd

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/asterisk/modules

%makeinstall_std

# Install configuration files
install -d %{buildroot}%{_sysconfdir}/asterisk
install -m0644 configs/cdr_mysql.conf.sample %{buildroot}%{_sysconfdir}/asterisk/cdr_mysql.conf
install -m0644 asterisk-ooh323c/h323.conf.sample %{buildroot}%{_sysconfdir}/asterisk/ooh323.conf
install -m0644 configs/res_mysql.conf.sample %{buildroot}%{_sysconfdir}/asterisk/res_mysql.conf

# fix docs
#cp format_mp3/MPGLIB_README MPGLIB_README.format_mp3
#cp format_mp3/MPGLIB_TODO MPGLIB_TODO.format_mp3
#cp format_mp3/README README.format_mp3
#cp asterisk-ooh323c/extensions.conf.sample extensions.conf.ooh323c
#cp asterisk-ooh323c/README README.ooh323c

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc doc/cdr_mysql.txt
%doc README
#doc MPGLIB_README.format_mp3 MPGLIB_TODO.format_mp3 README.format_mp3
#doc extensions.conf.ooh323c README.ooh323c
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/asterisk/cdr_mysql.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/asterisk/ooh323.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/asterisk/res_mysql.conf
%attr(0755,root,root) %{_libdir}/asterisk/modules/app_addon_sql_mysql.so
%attr(0755,root,root) %{_libdir}/asterisk/modules/app_saycountpl.so
%attr(0755,root,root) %{_libdir}/asterisk/modules/cdr_addon_mysql.so
%attr(0755,root,root) %{_libdir}/asterisk/modules/chan_ooh323.so
%attr(0755,root,root) %{_libdir}/asterisk/modules/format_mp3.so
%attr(0755,root,root) %{_libdir}/asterisk/modules/res_config_mysql.so



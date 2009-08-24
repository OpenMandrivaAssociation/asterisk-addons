%define	name	asterisk-addons
%define	version	1.6.1.1
%define asterisk_version 1.6.1.4
%define	release %mkrel %{asterisk_version}.2

Summary:	Additional addons for Asterisk
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Servers
URL:		http://www.asterisk.org/
Source:		http://downloads.asterisk.org/pub/telephony/asterisk/%{name}-%{version}.tar.gz
Source1:	menuselect.makeopts
Source2:	menuselect.makedeps
#Patch0:		asterisk-addons-1.4.0-mdk.diff
BuildRequires:	asterisk-devel = %{asterisk_version}
BuildRequires:	libtool
BuildRequires:	automake, autoconf
BuildRequires:	mysql-devel
BuildRequires:	ncurses-devel
Requires:	asterisk <= %{asterisk_version}
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Asterisk is a complete PBX in software. It runs on Linux and provides all of
the features you would expect from a PBX and more. Asterisk does voice over IP
in three protocols, and can interoperate with almost all standards-based
telephony equipment using relatively inexpensive hardware. This package
contains additional addons for asterisk.

%package -n asterisk-plugins-mobile
Summary:	Asterisk channel driver for bluetooth phones and headsets
Group:		System/Servers
BuildRequires:	libbluez-devel
Requires:	libbluez3
Requires:	asterisk = %{asterisk_version}
Provides:	asterisk-addons-plugins-modules = %{version}-%{release}

%description -n asterisk-plugins-mobile
Asterisk channel driver to allow Bluetooth cell/mobile phones to be
used as FXO devices, and headsets as FXS devices.

%prep

%setup -q -n %{name}-%{version}%{?beta:-rc%{beta}}
#%patch0 -p1
cp %{SOURCE1} menuselect.makedeps
cp %{SOURCE2} menuselect.makeopts

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
echo "%{version}" > build_tools/..version
echo "%{version}" > ..version
./bootstrap.sh
#autoreconf -fis
%configure \
	--with-bluetooth \
	--with-ncurses \
	--with-mysqlclient \
	--with-asterisk \
echo CFLAGS="%{optflags}" CXXFLAGS="%{optflags}"

make CFLAGS="%{optflags}" CXXFLAGS="%{optflags}"

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/asterisk
install -d %{buildroot}%{_libdir}/asterisk/modules
mkdir -p %{buildroot}%{_localstatedir}/lib/asterisk/documentation
%makeinstall samples
rm -f %{buildroot}%{_localstatedir}/lib/asterisk/documentation/*
rmdir %{buildroot}%{_localstatedir}/lib/asterisk/documentation
rmdir %{buildroot}%{_localstatedir}/lib/asterisk
rmdir %{buildroot}%{_localstatedir}/lib
rmdir %{buildroot}%{_localstatedir}

# Install configuration files
#install -m0644 configs/cdr_mysql.conf.sample %{buildroot}%{_sysconfdir}/asterisk/cdr_mysql.conf
#install -m0644 configs/res_mysql.conf.sample %{buildroot}%{_sysconfdir}/asterisk/res_mysql.conf
#install -m0644 configs/ooh323.conf.sample %{buildroot}%{_sysconfdir}/asterisk/ooh323.conf
#install -m0644 configs/mobile.conf.sample %{buildroot}%{_sysconfdir}/asterisk/mobile.conf

# fix docs
cp formats/mp3/MPGLIB_README MPGLIB_README.format_mp3
cp formats/mp3/MPGLIB_TODO MPGLIB_TODO.format_mp3
cp formats/mp3/README README.format_mp3

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc doc/ChangeLog.chan_ooh323 doc/cdr_mysql.txt doc/chan_ooh323.txt
%doc configs/*mysql.conf.sample configs/ooh323.conf.sample configs/mysql.conf.sample
%doc ChangeLog *README* UPGRADE.txt %{name}-%{version}-summary.txt
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/asterisk/cdr_mysql.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/asterisk/res_mysql.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/asterisk/mysql.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/asterisk/ooh323.conf
%attr(0755,root,root) %{_libdir}/asterisk/modules/app_addon_sql_mysql.so
%attr(0755,root,root) %{_libdir}/asterisk/modules/app_saycountpl.so
%attr(0755,root,root) %{_libdir}/asterisk/modules/cdr_addon_mysql.so
%attr(0755,root,root) %{_libdir}/asterisk/modules/chan_ooh323.so
%attr(0755,root,root) %{_libdir}/asterisk/modules/format_mp3.so
%attr(0755,root,root) %{_libdir}/asterisk/modules/res_config_mysql.so

%files -n asterisk-plugins-mobile
%defattr(-,root,root,-)
%doc doc/chan_mobile.txt configs/mobile.conf.sample
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/mobile.conf
%attr(0755,root,root) %{_libdir}/asterisk/modules/chan_mobile.so


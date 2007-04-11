Summary:	SIP proxy, redirect and registrar server
Summary(pl.UTF-8):	Serwer SIP rejestrujący, przekierowujący i robiący proxy
Name:		openser
Version:	1.2.0
Release:	1
License:	GPL v2
Group:		Networking/Daemons
Source0:	http://www.openser.org/pub/openser/%{version}/src/%{name}-%{version}-tls_src.tar.gz
# Source0-md5:	fbf929ed9d3ef1c3f41e4ebecbc4dd26
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-paths.patch
URL:		http://www.openser.org/
BuildRequires:	bison
BuildRequires:	expat-devel
BuildRequires:	flex
BuildRequires:	libpqxx-devel
BuildRequires:	libxml2-devel
BuildRequires:	mysql-devel
BuildRequires:	net-snmp-devel
BuildRequires:	openssl-devel
BuildRequires:	perl-devel
BuildRequires:	radiusclient-ng-devel
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	unixODBC-devel
#BuildRequires:	xmlrpc-c-devel >= 1.10.0
BuildRequires:	zlib-devel
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# mi_xmlrpc requires xmlrpc-c-devel in version 1.9 only
# osp needs Open settlement protocol implementation to be packaged (https://sourceforge.net/projects/osp-toolkit/)
%define	exclude_modules	mi_xmlrpc osp

%description
SIP Express Router (ser) is a high-performance, configurable, free SIP
(RFC 3261) server. It can act as registrar, proxy or redirect server.
OpenSER features an application-server interface, presence support,
SMS gateway, SIMPLE2Jabber gateway, RADIUS/syslog accounting and
authorization, server status monitoring, FCP security, etc. Web-based
user provisioning, serweb, available. Its performance allows it to
deal with operational burdens, such as broken network components,
attacks, power-up reboots and rapidly growing user population.
OpenSER's configuration ability meets needs of a whole range of
scenarios including small-office use, enterprise PBX replacements and
carrier services.

%description -l pl.UTF-8
SIP Express Router (ser) to wysoko wydajny, konfigurowalny, darmowy
serwer SIP (RFC 3261). Może działać jako serwer rejestrujący, proxy
lub przekierowujący. Możliwości OpenSER-a obejmują interfejs serwera
aplikacji, obsługę obecności, bramkę SMS, bramkę SIMPLE2Jabber,
rozliczanie przez RADIUS/syslog oraz autoryzację, monitorowanie stanu
serwera, bezpieczeństwo FCP itp. Jest dostępny oparty na WWW serwer
opiekujący się użytkownikami - serweb. Wydajność pozwala na raczenie
sobie z obciążeniem operacyjnym, takim jak uszkodzone elementy sieci,
ataki, zaniki zasilania i szybko rosnące grono użytkowników.
Możliwości konfiguracyjne OpenSER-a zaspokajają potrzeby w szerokim
zakresie scenariuszy włącznie z użyciem w małych biurach,
zastępowaniem poważnych PBX-ów i usług transportowych.

%package mysql
Summary:	OpenSER MySQL module
Summary(pl.UTF-8):	Moduł MySQL do OpenSER
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}

%description mysql
MySQL module for OpenSER.

%description mysql -l pl.UTF-8
Moduł MySQL do OpenSER.

%package postgres
Summary:	OpenSER PostgreSQL module
Summary(pl.UTF-8):	Moduł PostgreSQL do OpenSER
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}

%description postgres
PostgreSQL module for OpenSER.

%description postgres -l pl.UTF-8
Moduł PostgreSQL do OpenSER.

%package radius
Summary:	OpenSER Radius module
Summary(pl.UTF-8):	Moduł Radius do OpenSER
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}

%description radius
Radius module for OpenSER.

%description radius -l pl.UTF-8
Moduł Radius do OpenSER.

%package odbc
Summary:	OpenSER ODBC module
Summary(pl.UTF-8):	Moduł ODBC do OpenSER
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}

%description odbc
ODBC module for OpenSER.

%description odbc -l pl.UTF-8
Moduł ODBC do OpenSER.

%package perl
Summary:	OpenSER perl module
Summary(pl.UTF-8):	Moduł perl do OpenSER
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}

%description perl
Perl module for OpenSER.

%description perl -l pl.UTF-8
Moduł perl do OpenSER.

%package jabber
Summary:	OpenSER Jabber module
Summary(pl.UTF-8):	Moduł Jabber do OpenSER
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}

%description jabber
Jabber module for OpenSER.

%description jabber -l pl.UTF-8
Moduł Jabber do OpenSER.

%prep
%setup -q -n %{name}-%{version}-tls
%patch0 -p1

find -type d -name CVS | xargs rm -rf

%build
%{__make} all \
	exclude_modules="%{exclude_modules}" \
	CC="%{__cc}" \
	PREFIX="%{_prefix}" \
	CFLAGS="%{rpmcflags} -I/usr/include/xmlrpc-c -Wcast-align -fPIC" \
	TLS=1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{ser,sysconfig,rc.d/init.d}

%{__make} install \
	exclude_modules="%{exclude_modules}" \
	PREFIX="%{_prefix}" \
	basedir=$RPM_BUILD_ROOT

for i in modules/*; do \
	i=$(basename $i)
	[ -f modules/$i/README ] && cp -f modules/$i/README README.$i; \
done

#cd doc/serdev
#docbook2html serdev.sgml
#rm -f serdev.sgml
#cd ../seruser
#docbook2html seruser.sgml
#rm -f seruser.sgml
#cd ../..

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/openser
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/openser

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add openser
%service openser restart "sip Daemon"

%preun
if [ "$1" = "0" ]; then
	%service openser stop
	/sbin/chkconfig --del openser
fi

%files
%defattr(644,root,root,755)
%doc README* TODO scripts examples
%attr(755,root,root) %{_sbindir}/*
%exclude %{_sbindir}/openser_mysql.sh
%exclude %{_sbindir}/openser_postgresql.sh
%dir %{_sysconfdir}/openser
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/openser/openser.cfg
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/openser/openserctlrc
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/openser
%attr(754,root,root) /etc/rc.d/init.d/openser
%dir %{_libdir}/openser
%{_libdir}/openser/openserctl
%dir %{_libdir}/openser/modules
# explict list here, no globs please (to avoid mistakes)
%attr(755,root,root) %{_libdir}/openser/modules/acc.so
%attr(755,root,root) %{_libdir}/openser/modules/alias_db.so
%attr(755,root,root) %{_libdir}/openser/modules/auth.so
%attr(755,root,root) %{_libdir}/openser/modules/auth_db.so
%attr(755,root,root) %{_libdir}/openser/modules/auth_diameter.so
%attr(755,root,root) %{_libdir}/openser/modules/avpops.so
%attr(755,root,root) %{_libdir}/openser/modules/cpl-c.so
%attr(755,root,root) %{_libdir}/openser/modules/dbtext.so
%attr(755,root,root) %{_libdir}/openser/modules/dialog.so
%attr(755,root,root) %{_libdir}/openser/modules/dispatcher.so
%attr(755,root,root) %{_libdir}/openser/modules/diversion.so
%attr(755,root,root) %{_libdir}/openser/modules/domain.so
%attr(755,root,root) %{_libdir}/openser/modules/domainpolicy.so
%attr(755,root,root) %{_libdir}/openser/modules/enum.so
%attr(755,root,root) %{_libdir}/openser/modules/exec.so
%attr(755,root,root) %{_libdir}/openser/modules/flatstore.so
%attr(755,root,root) %{_libdir}/openser/modules/gflags.so
%attr(755,root,root) %{_libdir}/openser/modules/group.so
%attr(755,root,root) %{_libdir}/openser/modules/imc.so
%attr(755,root,root) %{_libdir}/openser/modules/lcr.so
%attr(755,root,root) %{_libdir}/openser/modules/mangler.so
%attr(755,root,root) %{_libdir}/openser/modules/maxfwd.so
%attr(755,root,root) %{_libdir}/openser/modules/mediaproxy.so
%attr(755,root,root) %{_libdir}/openser/modules/mi_fifo.so
%attr(755,root,root) %{_libdir}/openser/modules/msilo.so
%attr(755,root,root) %{_libdir}/openser/modules/nathelper.so
%attr(755,root,root) %{_libdir}/openser/modules/options.so
%attr(755,root,root) %{_libdir}/openser/modules/pa.so
%attr(755,root,root) %{_libdir}/openser/modules/path.so
%attr(755,root,root) %{_libdir}/openser/modules/pdt.so
%attr(755,root,root) %{_libdir}/openser/modules/permissions.so
%attr(755,root,root) %{_libdir}/openser/modules/pike.so
%attr(755,root,root) %{_libdir}/openser/modules/presence.so
%attr(755,root,root) %{_libdir}/openser/modules/pua.so
%attr(755,root,root) %{_libdir}/openser/modules/pua_mi.so
%attr(755,root,root) %{_libdir}/openser/modules/pua_usrloc.so
%attr(755,root,root) %{_libdir}/openser/modules/registrar.so
%attr(755,root,root) %{_libdir}/openser/modules/rr.so
%attr(755,root,root) %{_libdir}/openser/modules/seas.so
%attr(755,root,root) %{_libdir}/openser/modules/siptrace.so
%attr(755,root,root) %{_libdir}/openser/modules/sl.so
%attr(755,root,root) %{_libdir}/openser/modules/sms.so
%attr(755,root,root) %{_libdir}/openser/modules/snmpstats.so
%attr(755,root,root) %{_libdir}/openser/modules/speeddial.so
%attr(755,root,root) %{_libdir}/openser/modules/sst.so
%attr(755,root,root) %{_libdir}/openser/modules/statistics.so
%attr(755,root,root) %{_libdir}/openser/modules/textops.so
%attr(755,root,root) %{_libdir}/openser/modules/tlsops.so
%attr(755,root,root) %{_libdir}/openser/modules/tm.so
%attr(755,root,root) %{_libdir}/openser/modules/uac.so
%attr(755,root,root) %{_libdir}/openser/modules/uac_redirect.so
%attr(755,root,root) %{_libdir}/openser/modules/uri.so
%attr(755,root,root) %{_libdir}/openser/modules/uri_db.so
%attr(755,root,root) %{_libdir}/openser/modules/usrloc.so
%attr(755,root,root) %{_libdir}/openser/modules/xlog.so
%attr(755,root,root) %{_libdir}/openser/modules/xmpp.so
%{_mandir}/man*/*

%files jabber
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/openser/modules/jabber.so

%files mysql
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/openser_mysql.sh
%attr(755,root,root) %{_libdir}/openser/modules/mysql.so

%files postgres
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/openser_postgresql.sh
%attr(755,root,root) %{_libdir}/openser/modules/postgres.so

%files radius
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/openser/dictionary.radius
%attr(755,root,root) %{_libdir}/openser/modules/auth_radius.so
%attr(755,root,root) %{_libdir}/openser/modules/avp_radius.so
%attr(755,root,root) %{_libdir}/openser/modules/group_radius.so
%attr(755,root,root) %{_libdir}/openser/modules/uri_radius.so

%files odbc
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/openser/modules/unixodbc.so

%files perl
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/openser/modules/perl.so

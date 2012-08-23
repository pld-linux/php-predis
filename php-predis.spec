#
# Conditional build:
%bcond_without	tests		# build without tests

%ifarch sparc sparc64
%undefine	with_tests
%endif

%define		php_min_version 5.2.6
%define		modname	predis
%include	/usr/lib/rpm/macros.php
Summary:	Flexible and feature-complete PHP client library for Redis
Summary(pl.UTF-8):	%{modname} -
Name:		php-%{modname}
Version:	0.6.6
Release:	3
License:	BSD-like
Group:		Development/Languages/PHP
Source0:	http://github.com/nrk/predis/tarball/v%{version}-PHP5.2#/%{modname}-%{version}.tgz
# Source0-md5:	082528157e0a30dcccc1e844f43eb968
Source1:	run-tests.sh
Patch0:		tests.patch
URL:		https://github.com/nrk/predis/wiki
%{?with_tests:BuildRequires:	php-PHPUnit}
%{?with_tests:BuildRequires:	redis-server}
BuildRequires:	rpmbuild(macros) >= 1.519
BuildRequires:	sed >= 4.0
Requires:	php(core) >= %{php_min_version}
Requires:	php(pcre)
Requires:	php(spl)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Predis is a flexible and feature-complete PHP client library for the
Redis key-value database.

%prep
%setup -qc
mv *-predis-*/* .
%patch0 -p1
ln -s %{SOURCE1} .

%build
%if %{with tests}
sh -x run-tests.sh
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_data_dir},%{_examplesdir}/%{name}-%{version}}

cp -a lib/* $RPM_BUILD_ROOT%{php_data_dir}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG LICENSE TODO README.markdown
%{php_data_dir}/Predis.php
%{php_data_dir}/Predis_Compatibility.php
%{_examplesdir}/%{name}-%{version}

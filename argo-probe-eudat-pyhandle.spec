Name:		argo-probe-eudat-pyhandle
Version:	1.0
Release:	1%{?dist}
Summary:	Monitoring Metrics for B2HANDLE 
License:	GPLv3+
Packager:	Kyriakos Gkinis <kyrginis@admin.grnet.gr>

Source:		%{name}-%{version}.tar.gz
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}

Requires:	python
Requires:	python-argparse
Requires:	python-lxml
Requires:	python-simplejson
Requires:	perl
Requires:	perl-JSON

Requires:	python-defusedxml
Requires:	python-httplib2

%description
Monitoring metrics to check functionality of Handle service via pyhandle

%prep
%setup -q

%define _unpackaged_files_terminate_build 0 

%install

install -d %{buildroot}/%{_libexecdir}/argo/probes/eudat-pyhandle
install -m 755 * %{buildroot}/%{_libexecdir}/argo/probes/eudat-pyhandle/.


%files
%dir /%{_libexecdir}/argo
%dir /%{_libexecdir}/argo/probes/
%dir /%{_libexecdir}/argo/probes/eudat-pyhandle

%pre

%changelog
* Thu Feb 6 2025 Themis Zamani <themiszamani@gmail.com> - 0.9-4
- Initial version of the package

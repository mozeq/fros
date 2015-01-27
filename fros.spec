Name:           fros
Version:        1.1
Release:        1%{?dist}
Summary:        Universal screencasting frontend with pluggable support for various backends

%global commit 4f17dbbfe18081125b3f8099607899eaab87c2ec
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Group:          Applications/System
License:        GPLv2+
URL:            https://github.com/mozeq/fros
# this url is wrong, because github doesn't offer a space for downloadable archives :(
Source:         https://github.com/mozeq/fros/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
%if 0%{?suse_version}
BuildRequires:  python-devel
%else
BuildRequires:  python3-devel
%endif
BuildRequires:  python3-setuptools

%description
Universal screencasting frontend with pluggable support for various backends.
The goal is to provide an unified access to as many screencasting backends as
possible while still keeping the same user interface so the user experience
while across various desktops and screencasting programs is seamless.

%package recordmydesktop
Summary: fros plugin for screencasting using recordmydesktop as a backend
Group: Applications/System
Requires: %{name} = %{version}-%{release}

%description recordmydesktop
fros plugin for screencasting using recordmydesktop as a backend

%package gnome
Summary: fros plugin for screencasting using Gnome3 integrated screencaster
Group: Applications/System
Requires: %{name} = %{version}-%{release}

%description gnome
fros plugin for screencasting using Gnome3 integrated screencaster

%prep
%setup -qn %{name}-%{commit}

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build

%install
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT

%check
%{__python3} setup.py test


%files
%doc README COPYING
%dir %{python3_sitelib}/pyfros
%{python3_sitelib}/pyfros/*.py*
%dir %{python3_sitelib}/pyfros/__pycache__
%{python3_sitelib}/pyfros/__pycache__/*.cpython-%{python3_version_nodots}.py*
%dir %{python3_sitelib}/pyfros/plugins
%{python3_sitelib}/pyfros/plugins/__init__.*
%{python3_sitelib}/pyfros/plugins/const.*
%dir %{python3_sitelib}/pyfros/plugins/__pycache__
%{python3_sitelib}/pyfros/plugins/__pycache__/*.cpython-%{python3_version_nodots}.py*
# fros-1.0-py2.7.egg-info
%dir %{python3_sitelib}/%{name}-%{version}-py%{python3_version}.egg-info
%{python3_sitelib}/%{name}-%{version}-py%{python3_version}.egg-info/*
%{_bindir}/fros
%{_mandir}/man1/%{name}.1*

%files recordmydesktop
%{python3_sitelib}/pyfros/plugins/*recordmydesktop.*

%files gnome
%{python3_sitelib}/pyfros/plugins/*gnome.*

%changelog
* Tue Jan 27 2015 Jakub Filak <jmoskovc@redhat.com> 1.1-1
- switch to Python3

* Fri May 31 2013 Jiri Moskovcak <jmoskovc@redhat.com> 1.0-1
- initial rpm

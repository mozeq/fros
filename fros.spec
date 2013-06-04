Name:           fros
Version:        1.0
Release:        1%{?dist}
Summary:        Universal screencasting fronted with pluggable support for various backends

%global commit ea62d88880605e5167cb9ec7a343c4f022910df8
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Group:          Applications/System
License:        GPLv2+
URL:            https://github.com/mozeq/fros
# this url is wrong, because github doesn't offer a space for downloadable archives :(
Source:         https://github.com/mozeq/fros/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-setuptools
%if 0%{?with_python3}
BuildRequires:  python3-setuptools
%endif # if with_python3

%description
Universal screencasting fronted with pluggable support for various backends.
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
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%install
rm -rf %{buildroot}

%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT

%check
%{__python} setup.py test

%clean
rm -rf $RPM_BUILD_ROOT


%files
%doc README
%dir %{python_sitelib}/pyfros
%{python_sitelib}/pyfros/*.py*
%dir %{python_sitelib}/pyfros/plugins
%{python_sitelib}/pyfros/plugins/__init__.*
%{python_sitelib}/pyfros/plugins/const.*
# fros-1.0-py2.7.egg-info
%dir %{python_sitelib}/%{name}-%{version}-py2.7.egg-info
%{python_sitelib}/%{name}-%{version}-py2.7.egg-info/*
%{_bindir}/fros

%files recordmydesktop
%{python_sitelib}/pyfros/plugins/*recordmydesktop.*

%files gnome
%{python_sitelib}/pyfros/plugins/*gnome.*

%changelog
* Fri May 31 2013 Jiri Moskovcak <jmoskovc@redhat.com> 1.0-1
- initial rpm
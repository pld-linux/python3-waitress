#
# Conditional build:
%bcond_without	python2	# CPython 2.x module
%bcond_without	python3	# CPython 3.x module
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

%define 	module	waitress
Summary:	Waitress WSGI server
Summary(pl.UTF-8):	Serwer WSGI Waitress
Name:		python-%{module}
Version:	1.1.0
Release:	1
License:	ZPL v2.1
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/waitress/
Source0:	https://files.pythonhosted.org/packages/source/w/waitress/%{module}-%{version}.tar.gz
# Source0-md5:	0f1eb7fdfdbf2e6d18decbda1733045c
URL:		https://docs.pylonsproject.org/projects/waitress/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.3
BuildRequires:	python3-setuptools
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg-3
BuildRequires:	python-pylons-sphinx-themes >= 0.3
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Waitress is meant to be a production-quality pure-Python WSGI server
with very acceptable performance.

%description -l pl.UTF-8
Waitress jest serwerem WSGI tworzonym w czystym Pythonie, z myślą o
produkcyjnej jakości i akceptowalnej wydajności.

%package -n python3-%{module}
Summary:	Waitress WSGI server
Summary(pl.UTF-8):	Serwer WSGI Waitress
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.3

%description -n python3-%{module}
Waitress is meant to be a production-quality pure-Python WSGI server
with very acceptable performance.

%description -n python3-%{module} -l pl.UTF-8
Waitress jest serwerem WSGI tworzonym w czystym Pythonie, z myślą o
produkcyjnej jakości i akceptowalnej wydajności.

%package apidocs
Summary:	API documentation for Python waitress module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona waitress
Group:		Documentation

%description apidocs
API documentation for Python waitress module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona waitress.

%prep
%setup -q -n %{module}-%{version}

# gives tcp connect errors
%{__mv} %{module}/tests/test_functional.py{,.disable}

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-2
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/waitress-serve{,-2}

%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/%{module}/tests
%py_postclean
%endif

%if %{with python3}
%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/waitress-serve{,-3}

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/%{module}/tests
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.txt COPYRIGHT.txt HISTORY.txt LICENSE.txt README.rst TODO.txt
%attr(755,root,root) %{_bindir}/waitress-serve-2
%{py_sitescriptdir}/waitress
%{py_sitescriptdir}/waitress-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGES.txt COPYRIGHT.txt HISTORY.txt LICENSE.txt README.rst TODO.txt
%attr(755,root,root) %{_bindir}/waitress-serve-3
%{py3_sitescriptdir}/waitress
%{py3_sitescriptdir}/waitress-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif

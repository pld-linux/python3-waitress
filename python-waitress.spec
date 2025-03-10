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
# keep 1.x here for python2 support
Version:	1.4.4
Release:	2
License:	ZPL v2.1
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/waitress/
Source0:	https://files.pythonhosted.org/packages/source/w/waitress/%{module}-%{version}.tar.gz
# Source0-md5:	079c3c4902b1cb5d0a917276ee70f1df
URL:		https://docs.pylonsproject.org/projects/waitress/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools >= 1:41
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools >= 1:41
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg-3 >= 1.8.1
BuildRequires:	python3-docutils
BuildRequires:	python3-pylons-sphinx-themes >= 1.0.9
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
Requires:	python3-modules >= 1:3.5

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

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTHONPATH=$(pwd)/src \
%{__python} -m unittest discover -s tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd)/src \
%{__python3} -m unittest discover -s tests
%endif
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/waitress-serve{,-2}

%py_postclean
%endif

%if %{with python3}
%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/waitress-serve{,-3}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.txt COPYRIGHT.txt HISTORY.txt LICENSE.txt README.rst
%attr(755,root,root) %{_bindir}/waitress-serve-2
%{py_sitescriptdir}/waitress
%{py_sitescriptdir}/waitress-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGES.txt COPYRIGHT.txt HISTORY.txt LICENSE.txt README.rst
%attr(755,root,root) %{_bindir}/waitress-serve-3
%{py3_sitescriptdir}/waitress
%{py3_sitescriptdir}/waitress-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif

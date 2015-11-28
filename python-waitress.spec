#
# Conditional build:
%bcond_without	tests	# do not perform "make test"

%define 	module	waitress
Summary:	Waitress WSGI server
Name:		python-%{module}
Version:	0.8.2
Release:	2
License:	ZPL 2.1
Group:		Libraries/Python
Source0:	http://pypi.python.org/packages/source/w/waitress/%{module}-%{version}.tar.gz
# Source0-md5:	2d924c85bc1005174da1d14294fcc663
URL:		http://docs.pylonsproject.org/projects/waitress/
BuildRequires:	python-distribute
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Waitress is meant to be a production-quality pure-Python WSGI server
with very acceptable performance.

%prep
%setup -q -n %{module}-%{version}

# gives tcp connect errors
mv %{module}/tests/test_functional.py{,.disable}

%build
%py_build

%{?with_tests:PYTHONPATH=build/lib %{__python} setup.py test}

%install
rm -rf $RPM_BUILD_ROOT
%py_install

%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/%{module}/tests

%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.txt LICENSE.txt README.rst TODO.txt
%dir %{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}/*.py[co]
%{py_sitescriptdir}/%{module}-%{version}*.egg-info

%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Summary: ANother Tool for Language Recognition
Name: antlr3
Version: 3.1.1
Release: 5%{?dist}
URL: http://www.antlr.org/
Source0: http://www.antlr.org/download/antlr-3.1.1.tar.gz
# Utility file, in conversation with upstream about this
Source1: antlr-clean-generated
Source2: antlr3
License: BSD
Group: Development/Libraries
BuildArch: noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: java-devel >= 1:1.6.0
# For cleaner script
BuildRequires: python
BuildRequires: ant, stringtemplate, ant-antlr, ant-junit
# The build.xml uses this to version the jar
BuildRequires: bcel
BuildRequires: jpackage-utils
Requires: jpackage-utils
Requires: antlr
Requires: stringtemplate

%description
ANother Tool for Language Recognition, is a language tool
that provides a framework for constructing recognizers,
interpreters, compilers, and translators from grammatical 
descriptions containing actions in a variety of target languages.

%package        python
Group:          Development/Libraries
Summary:        Python runtime support for ANTLR-generated parsers
BuildRequires:  python-devel
BuildRequires:  python-setuptools-devel
BuildArch:      noarch

%description    python
Python runtime support for ANTLR-generated parsers

%prep
%setup -q -n antlr-%{version}

%build
rm -f lib/*.jar
build-jar-repository -s -p lib stringtemplate bcel
# Clean out generated files upstream includes
%{__python} %{SOURCE1} .
# Build
ant

# Build the python runtime
cd runtime/Python
%{__python} setup.py build
cd ../..

%install
rm -rf $RPM_BUILD_ROOT
install -D build/antlr-3.1.1.jar $RPM_BUILD_ROOT%{_datadir}/java/antlr3.jar
install -D -m 0755 %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/antlr3

cd runtime/Python
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
cd ../..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README.txt LICENSE.txt
%{_datadir}/java/*.jar
%{_bindir}/antlr3

%files python
%defattr(0644,root,root,0755)
%{python_sitelib}/antlr3/*
%{python_sitelib}/antlr_python_runtime-*

%changelog
* Mon Jan 12 2009 Colin Walters <walters@redhat.com> - 3.1.1-5
- Add bcel to build path

* Mon Jan 12 2009 Colin Walters <walters@redhat.com> - 3.1.1-4
- Add bcel build dep to version jar name

* Mon Nov 10 2008 Colin Walters <walters@redhat.com> - 3.1.1-3
- Add antlr3 script

* Mon Nov  6 2008 Bart Vanbrabant <bart.vanbrabant@zoeloelip.be> - 3.1.1-2
- Fix the install of the jar (remove the version)

* Mon Nov  3 2008 Bart Vanbrabant <bart.vanbrabant@zoeloelip.be> - 3.1.1-1
- Update to version 3.1.1
- Add python runtime subpackage

* Fri Jun 27 2008 Colin Walters <walters@redhat.com> - 3.0.1-2
- Fix some BRs

* Sun Apr 06 2008 Colin Walters <walters@redhat.com> - 3.0.1-1
- First version

Summary: ANother Tool for Language Recognition
Name: antlr3
Version: 3.0.1
Release: 2%{?dist}
URL: http://www.antlr.org/
Source0: http://www.antlr.org/download/antlr-3.0.1.tar.gz
# Utility file, in conversation with upstream about this
Source1: antlr-clean-generated
License: BSD
Group: Development/Libraries
BuildArch: noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: java-devel >= 1:1.6.0
# For cleaner script
BuildRequires: python
BuildRequires: ant, stringtemplate, ant-antlr, ant-junit
BuildRequires: jpackage-utils
Requires: jpackage-utils

%description
ANother Tool for Language Recognition, is a language tool
that provides a framework for constructing recognizers,
interpreters, compilers, and translators from grammatical 
descriptions containing actions in a variety of target languages.

%prep
%setup -q -n antlr-%{version}

%build
rm -f lib/*.jar
build-jar-repository -s -p lib stringtemplate
# Clean out generated files upstream includes
python %{SOURCE1} .
# Build
ant

%install
rm -rf $RPM_BUILD_ROOT
install -D build/antlr.jar $RPM_BUILD_ROOT%{_datadir}/java/antlr3.jar

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README.txt LICENSE.txt
%{_datadir}/java/*.jar

%changelog
* Fri Jun 27 2008 Colin Walters <walters@redhat.com> - 3.0.1-2
- Fix some BRs

* Sun Apr 06 2008 Colin Walters <walters@redhat.com> - 3.0.1-1
- First version

%{?scl:%scl_package antlr3}
%{!?scl:%global pkg_name %{name}}

%global antlr_version 3.5.2
%global c_runtime_version 3.4
%global javascript_runtime_version 3.1
%global baserelease 14

%{!?_with_bootstrap: %global bootstrap 1}

Name:           %{?scl_prefix}antlr3
Epoch:          1
Version:        %{antlr_version}
Release:        %{baserelease}%{?dist}
Summary:        ANother Tool for Language Recognition
License:        BSD
URL:            http://www.antlr3.org/

Source0:        https://github.com/antlr/%{pkg_name}/archive/%{antlr_version}.tar.gz
#Source2:        http://www.antlr3.org/download/Python/antlr_python_runtime-%{python_runtime_version}.tar.gz
Source3:        http://www.antlr3.org/download/antlr-javascript-runtime-%{javascript_runtime_version}.zip

%if 0%{?bootstrap}
# generate with:
# mock -i antlr3-tool stringtemplate
# (cd `mock -p` && tar cjf $OLDPWD/antlr3-prebuilt.tar.bz2 usr/share/{maven-metadata,java}/{antlr3,stringtemplate}*)
Source9999:	antlr3-prebuilt.tar.bz2
%endif

Patch0:         0001-java8-fix.patch
# Generate OSGi metadata
Patch1:         osgi-manifest.patch
# remove dot option
Patch2:         remove_dot_option.patch

BuildRequires:  %{?scl_prefix_maven}maven-local
BuildRequires:  %{?scl_prefix_maven}maven-plugin-bundle
BuildRequires:  %{?scl_prefix_maven}maven-plugin-plugin
BuildRequires:  %{?scl_prefix_maven}maven-project
BuildRequires:  %{?scl_prefix_maven}plexus-compiler
BuildRequires:  %{?scl_prefix_maven}sonatype-oss-parent

%if ! 0%{?bootstrap}
BuildRequires:  mvn(org.antlr:ST4)
BuildRequires:  mvn(org.antlr:stringtemplate)
BuildRequires:  mvn(org.antlr:antlr)
BuildRequires:  mvn(org.antlr:antlr3-maven-plugin)
%endif

BuildRequires:  %{?scl_prefix_maven}xmvn
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
%{?scl:Requires: %scl_runtime}

# we don't build it now
Obsoletes:      %{pkg_name}-gunit < 3.2-15

%description
ANother Tool for Language Recognition, is a language tool
that provides a framework for constructing recognizers,
interpreters, compilers, and translators from grammatical
descriptions containing actions in a variety of target languages.

%package tool
Summary:        ANother Tool for Language Recognition
BuildArch:      noarch
Provides:       %{pkg_name} = %{epoch}:%{antlr_version}-%{release}
Obsoletes:      %{pkg_name} < %{epoch}:%{antlr_version}-%{release}
Requires:       %{pkg_name}-java = %{epoch}:%{antlr_version}-%{release}

Provides:       ant-%{pkg_name} = %{epoch}:%{antlr_version}-%{release}
Obsoletes:      ant-%{pkg_name} < %{epoch}:%{antlr_version}-%{release}

%description tool
ANother Tool for Language Recognition, is a language tool
that provides a framework for constructing recognizers,
interpreters, compilers, and translators from grammatical
descriptions containing actions in a variety of target languages.

%package java
Summary:        Java run-time support for ANTLR-generated parsers
BuildArch:      noarch

%description java
Java run-time support for ANTLR-generated parsers

%package javadoc
Summary:        API documentation for %{name}
BuildArch:      noarch

%description javadoc
%{summary}.

%package javascript
Summary:        Javascript run-time support for ANTLR-generated parsers
Version:        %{javascript_runtime_version}
Release:        %{antlr_version}.%{baserelease}%{?dist}
BuildArch:      noarch

%description  javascript
Javascript run-time support for ANTLR-generated parsers

%package C
Summary:        C run-time support for ANTLR-generated parsers
Version:        %{c_runtime_version}
Release:        %{antlr_version}.%{baserelease}%{?dist}

%description C
C run-time support for ANTLR-generated parsers

%package C-devel
Summary:        Header files for the C bindings for ANTLR-generated parsers
Requires:       %{pkg_name}-C = %{epoch}:%{c_runtime_version}-%{release}
Version:        %{c_runtime_version}
Release:        %{antlr_version}.%{baserelease}%{?dist}

%description C-devel
Header files for the C bindings for ANTLR-generated parsers

%package C-docs
Summary:        API documentation for the C run-time support for ANTLR-generated parsers
BuildArch:      noarch
BuildRequires:  graphviz
BuildRequires:  doxygen
Requires:       %{pkg_name}-C = %{epoch}:%{c_runtime_version}-%{release}
Version:        %{c_runtime_version}
Release:        %{antlr_version}.%{baserelease}%{?dist}

%description C-docs
This package contains doxygen documentation with instruction
on how to use the C target in ANTLR and complete API description of the
C run-time support for ANTLR-generated parsers.

%package C++-devel
Summary:        C++ runtime support for ANTLR-generated parsers

%description C++-devel
C++ runtime support for ANTLR-generated parsers.

%prep
%setup -q -n %{pkg_name}-%{antlr_version} -a 3
sed -i "s,\${buildNumber},`cat %{_sysconfdir}/fedora-release` `date`," tool/src/main/resources/org/antlr/antlr.properties
%patch0 -p1
%patch1 -p1
# remove dot option for scl package
%{?scl:%patch2 -p1}
%{?scl:rm runtime/Java/src/main/java/org/antlr/runtime/tree/DOTTreeGenerator.java}

# remove pre-built artifacts
find -type f -a -name *.jar -delete
find -type f -a -name *.class -delete

%if 0%{?bootstrap}
mkdir bootstrap-repo
tar xf %{SOURCE9999} -C bootstrap-repo
sed -i "s:/usr/share/:$PWD/bootstrap-repo&:g" bootstrap-repo/usr/share/maven-metadata/*.xml
sed -i "/optional/d" bootstrap-repo/usr/share/maven-metadata/*.xml
mkdir -p .xmvn/config.d
cat > .xmvn/config.d/bootstrap-config.xml <<EOF
<configuration>
<resolverSettings>
  <metadataRepositories>
    <repository>$PWD/bootstrap-repo/usr/share/maven-metadata</repository>
  </metadataRepositories>
</resolverSettings>
</configuration>
EOF
%endif

%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%pom_disable_module %{pkg_name}-maven-archetype
%pom_disable_module gunit
%pom_disable_module gunit-maven-plugin
%pom_disable_module antlr-complete

%pom_remove_plugin :maven-source-plugin
%pom_remove_plugin :maven-javadoc-plugin

# compile for target 1.6, see BZ#842572
sed -i 's/jsr14/1.6/' %{pkg_name}-maven-archetype/src/main/resources/archetype-resources/pom.xml \
                      %{pkg_name}-maven-plugin/pom.xml \
                                          gunit/pom.xml \
                                          gunit-maven-plugin/pom.xml \
                                          pom.xml \
                                          runtime/Java/pom.xml \
                                          tool/pom.xml

# workarounds bug in filtering (Mark invalid)
%pom_xpath_remove pom:resource/pom:filtering

%mvn_package :antlr-runtime java
%mvn_package : tool

%mvn_file :antlr %{pkg_name}
%mvn_file :antlr-runtime %{pkg_name}-runtime
%mvn_file :antlr-maven-plugin %{pkg_name}-maven-plugin
%{?scl:EOF}

%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_build -f

# Build the C runtime
pushd runtime/C
autoreconf -i
%configure --disable-abiflags --enable-debuginfo \
%if 0%{?__isa_bits} == 64
    --enable-64bit
%else
    %{nil}
%endif

sed -i "s#CFLAGS = .*#CFLAGS = $RPM_OPT_FLAGS#" Makefile
make %{?_smp_mflags}
doxygen -u # update doxygen configuration file
doxygen # build doxygen documentation
popd

# build ant task
pushd antlr-ant/main/%{pkg_name}-task/
export CLASSPATH=$(build-classpath ant)
javac -encoding ISO-8859-1 %{pkg_name}-src/org/apache/tools/ant/antlr/ANTLR3.java
jar cvf ant-%{pkg_name}.jar \
  -C %{pkg_name}-src org/apache/tools/ant/antlr/antlib.xml \
  -C %{pkg_name}-src org/apache/tools/ant/antlr/ANTLR3.class
popd
%{?scl:EOF}

%install
mkdir -p $RPM_BUILD_ROOT/%{_mandir}
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/antlr

%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_install
%{?scl:EOF}

# install ant task
install -m 644 antlr-ant/main/%{pkg_name}-task/ant-%{pkg_name}.jar -D $RPM_BUILD_ROOT%{_javadir}/ant/ant-%{pkg_name}.jar
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ant.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/ant.d/ant-%{pkg_name} << EOF
ant/ant-%{pkg_name} %{pkg_name}
EOF

# install wrapper script
%jpackage_script org.antlr.Tool '' '' 'stringtemplate4/ST4.jar:%{pkg_name}.jar:%{pkg_name}-runtime.jar' %{pkg_name} true

# install C runtime
pushd runtime/C
make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT%{_libdir}/libantlr3c.{a,la}
pushd api/man/man3
for file in `ls -1 * | grep -vi "^antlr3"`; do
    mv $file antlr3-$file
done
sed -i -e 's,^\.so man3/pANTLR3,.so man3/antlr3-pANTLR3,' `grep -rl 'man3/pANTLR3' .`
gzip *
popd
mv api/man/man3 $RPM_BUILD_ROOT%{_mandir}/
rmdir api/man
popd

# install javascript runtime
pushd antlr-javascript-runtime-%{javascript_runtime_version}
install -pm 644 *.js $RPM_BUILD_ROOT%{_datadir}/antlr/
popd

# install C++ runtime (header only)
mkdir -p $RPM_BUILD_ROOT/%{_includedir}/%{pkg_name}
install -pm 644 runtime/Cpp/include/* $RPM_BUILD_ROOT/%{_includedir}/

%post C -p /sbin/ldconfig

%postun C -p /sbin/ldconfig

%files tool -f .mfiles-tool
%doc README.txt tool/{LICENSE.txt,CHANGES.txt}
%{_bindir}/%{pkg_name}
%{_javadir}/ant/ant-%{pkg_name}.jar
%config(noreplace) %{_sysconfdir}/ant.d/ant-%{pkg_name}

%files C
%doc tool/LICENSE.txt
%{_libdir}/libantlr3c.so

%files C-devel
%{_mandir}/man3/*
%{_includedir}/*.h

%files C-docs
%doc runtime/C/api

%files C++-devel
%doc tool/LICENSE.txt
%{_includedir}/*.hpp
%{_includedir}/*.inl

%files java -f .mfiles-java
%doc tool/LICENSE.txt

%files javascript
%doc tool/LICENSE.txt
%{_datadir}/antlr/

%files javadoc -f .mfiles-javadoc
%doc tool/LICENSE.txt

%changelog
* Mon Nov 28 2016 Tomas Repik <trepik@redhat.com> - 1:3.5.2-14
- scl conversion

* Tue Oct 04 2016 David Geiger <daviddavid> - 1:3.5.2-13
- Fix stringtemplate4 jar classpath in shell script (stringtemplate4/ST4.jar)

* Tue Sep 27 2016 Michael Simacek <msimacek@redhat.com> - 1:3.5.2-12
- Fix Java 8 patch

* Wed Jun 15 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.5.2-11
- Regenerate build-requires

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.5.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 24 2015 Mat Booth <mat.booth@redhat.com> - 1:3.5.2-10
- Fix OSGi metadata
- Delete some commented out sections

* Wed Jun 17 2015 Mat Booth <mat.booth@redhat.com> - 1:3.5.2-9
- Build and ship the antlr3 ant task
- Add provides/obsoletes for separate ant-antlr3 package

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.5.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 29 2015 Michal Srb <msrb@redhat.com> - 1:3.5.2-7
- Fix FTBFS (Resolves: rhbz#1204672)

* Mon Mar 30 2015 Michael Simacek <msimacek@redhat.com> - 1:3.5.2-6
- Fix FTBFS

* Mon Mar 23 2015 Dan Horák <dan[at]danny.cz> - 1:3.5.2-5
- update BR - whole autotools chain is required explicitly

* Fri Oct 31 2014 Yaakov Selkowitz <yselkowi@redhat.com> - 1:3.5.2-4
- Avoid timestamp conflicts when updating jar manifest

* Sun Aug 31 2014 Till Maas <opensource@till.name> - 1:3.5.2-3
- Add missing dist tags for subpackages

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jun 18 2014 Michael Simacek <msimacek@redhat.com> - 3.5.2-1
- Update to upstream version 3.5.2
- Build the C runtime from main tarball
- Make C++-devel subpackage

* Tue Jun 17 2014 Michael Simacek <msimacek@redhat.com> - 3.5-1
- Update to upstream version 3.5

* Tue Jun 17 2014 Michael Simacek <msimacek@redhat.com> - 3.4-18
- Specfile cleanup

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.4-16
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 3.4-13
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Sun Sep 09 2012 Miloš Jakubíček <xjakub@fi.muni.cz> - 3.4-12
- Fix wrong man page references (see BZ#855619)

* Tue Aug 21 2012 Miloš Jakubíček <xjakub@fi.muni.cz> - 3.4-11
- Now really compile for Java 1.6 everything

 *Sat Aug 18 2012 Miloš Jakubíček <xjakub@fi.muni.cz> - 3.4-10
- Explicitly compile for Java 1.5, to (maybe?) fix BZ#842572

* Mon Aug 6 2012 Alexander Kurtakov <akurtako@redhat.com> 3.4-9
- Inject org.antlr.runtime OSGi metadata.
- Update BRs to newer versions.

* Tue Jul 24 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.4-8
- Add back requires on stringtemplate for java subpackage

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 26 2012 Miloš Jakubíček <xjakub@fi.muni.cz> - 3.4-6
- Fixed missing stringtemplate4 in antlr3 generator classpath
- Cleanup of Requires and BuildRequires on antlr2

* Thu Feb 23 2012 Miloš Jakubíček <xjakub@fi.muni.cz> - 3.4-5
- Disable python runtime (incompatible with current antlr version)

* Wed Feb 22 2012 Miloš Jakubíček <xjakub@fi.muni.cz> - 3.4-4
- Fix permissions for egg-info dir (fixes BZ#790499)

* Thu Feb 16 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.4-3
- Use wildcards for installing jars (different results on different releases)

* Thu Feb 16 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.4-2
- Add builnumber plugin to buildrequires
- Tab/space cleanup

* Mon Jan 23 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.4-1
- Update antlr version to 3.4
- Move to maven3 build, update macros etc
- Remove gunit for now

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Sep 09 2011 Dan Horák <dan[at]danny.cz> - 3.2-15
- fix build on other arches

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 14 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.2-13
- Add stringtemplate to Requires of java subpackage
- Use tomcat6 for building
- Use felix-parent and cleanup BRs on maven plugins

* Thu Nov 25 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.2-12
- Move all pom files into java subpackage
- Fix pom filenames (Resolves rhbz#655831)
- Add java subpackage Requires for gunit subpackage

* Wed Oct 13 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 3.2-11
- non-bootstrap build

* Wed Oct 13 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 3.2-10
- fix pom patch
- fix bootstrapping
- fix dependencies

* Wed Aug 11 2010 David Malcolm <dmalcolm@redhat.com> - 3.2-9
- recompiling .py files against Python 2.7 (rhbz#623269)

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 3.2-8
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jun 17 2010 Lubomir Rintel <lkundrak@v3.sk> - 3.2-7
- Add master and runtime poms (#605267)

* Sat May 01 2010 Miloš Jakubíček <xjakub@fi.muni.cz> - 3.2-6
- Patch the Python runtime to print just a warning in case of version mismatch
  instead of raising an exception (since there is a good change it will work).

* Thu Apr 22 2010 Miloš Jakubíček <xjakub@fi.muni.cz> - 3.2-5
- Build the C runtime with --enable-64bit on x86_64 to avoid undeterministic
  segfaults caused by possible invalid conversion of 64bit pointers to int32_t

* Mon Mar 08 2010 Miloš Jakubíček <xjakub@fi.muni.cz> - 3.2-4
- Patch Java runtime build to include OSGi meta-information in the manifest
  (thanks to Mat Booth)
- Add "antlr3" prefix to all man pages to prevent namespace conflicts with
  standard man pages included in the man-pages package
- Split headers and man pages into a C-devel subpackage
- Fix multiple file ownership of Java runtime and gunit by the tool package

* Tue Mar 02 2010 Miloš Jakubíček <xjakub@fi.muni.cz> - 3.2-3
- Rebuilt in non-bootstrap mode.

* Sun Jan 31 2010 Milos Jakubicek <xjakub@fi.muni.cz> - 3.2-2
- Build the doxygen documentation for the C target in a C-docs subpackage
- BuildRequires/Requires cleanup across subpackages

* Sat Jan 30 2010 Milos Jakubicek <xjakub@fi.muni.cz> - 3.2-1
- Update to 3.2, bootstrap build.
- Build bindings for C and JavaScript as well as gunit and maven plugin.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 17 2009 Bart Vanbrabant <bart.vanbrabant@zoeloelip.be> - 3.1.1-7
- Fix the name of the jar to antlr.jar

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 12 2009 Colin Walters <walters@redhat.com> - 3.1.1-5
- Add bcel to build path

* Mon Jan 12 2009 Colin Walters <walters@redhat.com> - 3.1.1-4
- Add bcel build dep to version jar name

* Mon Nov 10 2008 Colin Walters <walters@redhat.com> - 3.1.1-3
- Add antlr3 script

* Thu Nov  6 2008 Bart Vanbrabant <bart.vanbrabant@zoeloelip.be> - 3.1.1-2
- Fix the install of the jar (remove the version)

* Mon Nov  3 2008 Bart Vanbrabant <bart.vanbrabant@zoeloelip.be> - 3.1.1-1
- Update to version 3.1.1
- Add python runtime subpackage

* Fri Jun 27 2008 Colin Walters <walters@redhat.com> - 3.0.1-2
- Fix some BRs

* Sun Apr 06 2008 Colin Walters <walters@redhat.com> - 3.0.1-1
- First version

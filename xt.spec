%define section            free
%define gcj_support        1

Name:           xt
Version:        20051206
Release:        %mkrel 1.4
Epoch:          0
Summary:        Fast, free implementation of XSLT in Java
License:        BSD-style
Group:          Development/Java
Source0:        http://www.blnz.com/xt/xt-20051206-src.tar.bz2
Source1:        xt-build.xml
Patch0:         xt-20050823-build.patch
Url:            http://www.blnz.com/xt/index.html
Requires:       servletapi5
Requires:       xerces-j2
Requires:       xml-commons-jaxp-1.3-apis
BuildRequires:  ant
BuildRequires:  java-rpmbuild >= 0:1.5
BuildRequires:  servletapi5
BuildRequires:  xerces-j2
BuildRequires:  xml-commons-jaxp-1.3-apis
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildRequires:    java-devel
BuildArch:        noarch
%endif
Obsoletes:        xt-dash < %{version}
Provides:         xt-dash = %{version}

%description
XT is an implementation in Java of XSL Transformations.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%if 0
%package demo
Summary:        Demo for %{name}
Requires:       %{name} = %{epoch}:%{version}-%{release}
Group:          Development/Java

%description demo
Demonstrations and samples for %{name}.
%endif

%prep
%setup -q
%{__rm} src/xt/java/com/jclark/xsl/trax/UriResolverAdapter.java
%{__rm} src/xt/java/com/jclark/xsl/trax/TraxUtil.java
%patch0 -p1

# replace included build.xml
%{__cp} -a %{SOURCE1} build.xml
%{__perl} -pi -e 's/<javac/<javac nowarn="true"/g' build.xml
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;
%{__rm} -r docs thirdparty
%{__perl} -pi -e 's/enum/en/g' `%{_bindir}/find . -name '*.java'`

%build
export CLASSPATH=$(build-classpath servletapi5 xerces-j2 xml-commons-jaxp-1.3-apis)
%{ant} jar javadoc

%install
%{__rm} -rf %{buildroot}

# jars
%{__mkdir_p} %{buildroot}%{_javadir}
%{__cp} -a build/lib/%{name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && %{__ln_s} %{name}-%{version}.jar %{name}-dash-%{version}.jar)
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do %{__ln_s} ${jar} ${jar/-%{version}/}; done)

# javadoc
%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__cp} -a build/api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
(cd %{buildroot}%{_javadocdir} && %{__ln_s} %{name}-%{version} %{name})

# data
%if 0
%{__mkdir_p} %{buildroot}%{_datadir}/%{name}
%{__cp} -a demo %{buildroot}%{_datadir}/%{name}
%endif

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%{__perl} -pi -e 's/\r$//g' *.txt *.html

%clean
%{__rm} -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc *.txt *.html
%{_javadir}/*.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-%{version}.jar.*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %dir %{_javadocdir}/%{name}

%if 0
%files demo
%defattr(0644,root,root,0755)
%{_datadir}/%{name}
%endif

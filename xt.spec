%define gcj_support	1
%define base_name	xt
%define name		%{base_name}
%define version		20051206
%define release		%mkrel 1
%define	section		free

Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		0
Summary:	A fast, free implementation of XSLT in Java
License:	BSD style
Group:		Development/Java
Source0:	http://www.blnz.com/xt/xt-20051206-src.tar.bz2
Source1:	xt-build.xml
Patch0:		xt-20050823-build.patch.bz2
Url:		http://www.blnz.com/xt/index.html
Requires:	servletapi5
Requires:	xerces-j2
Requires:	xml-commons-apis
BuildRequires:	ant
BuildRequires:	java-devel
BuildRequires:	jpackage-utils >= 0:1.5
BuildRequires:	servletapi5
BuildRequires:	xerces-j2
BuildRequires:	xml-commons-apis
%if %{gcj_support}
Requires(post):	java-gcj-compat
Requires(postun): java-gcj-compat
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:	noarch
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
#Distribution:	JPackage
#Vendor:		JPackage Project
Obsoletes:	xt-dash
Provides:	xt-dash

%description
XT is an implementation in Java of XSL Transformations.

%package javadoc
Summary:	Javadoc for %{name}
Group:		Development/Java

%description javadoc
Javadoc for %{name}.

%if 0
%package demo
Summary:	Demo for %{name}
Requires:	%{name} = %{version}-%{release}
Group:		Development/Java

%description demo
Demonstrations and samples for %{name}.
%endif

%prep
%setup -q
%patch0 -p1
# replace included build.xml
install -m 644 %{SOURCE1} build.xml
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;
%{__rm} -rf docs thirdparty

%build
export CLASSPATH=$(build-classpath servletapi5 xerces-j2 xml-commons-apis)
%ant jar
%ant javadoc

%install
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 build/lib/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} ${jar/-%{version}/}; done)
(cd $RPM_BUILD_ROOT%{_javadir} && ln -sf %{name}-%{version}.jar %{name}-dash.jar)
# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
# data
%if 0
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -pr demo $RPM_BUILD_ROOT%{_datadir}/%{name}
%endif

%if %{gcj_support}
aot-compile-rpm
%endif

%{__perl} -pi -e 's/\r$//g' *.txt *.html

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{_bindir}/rebuild-gcj-db

%postun
%{_bindir}/rebuild-gcj-db
%endif

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ "$1" = "0" ]; then
    rm -f %{_javadocdir}/%{name}
fi

%files
%defattr(0644,root,root,0755)
%doc *.txt *.html
%{_javadir}/*.jar
%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-%{version}.jar.*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}

%if 0
%files demo
%defattr(0644,root,root,0755)
%{_datadir}/%{name}
%endif

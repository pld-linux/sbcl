Summary:	The Steel Bank Common Lisp development environment
Summary(pl):	¦rodowisko programowania Steel Bank Common Lisp
Name:		sbcl
Version:	0.8.1
Release:	1
License:	MIT
Group:		Development/Languages
Source0:	http://dl.sourceforge.net/sbcl/%{name}-%{version}-source.tar.bz2
# Source0-md5:	884771bd1ac26bc78c897ae6510541d9
URL:		http://sbcl.sourceforge.net/
BuildRequires:	sbcl
BuildRequires:	docbook-utils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Steel Bank Common Lisp (SBCL) is a Open Source development environment
for Common Lisp based on CMUCL. It includes an integrated native compiler,
interpreter, and debugger.

%description -l pl
Steel Bank Common Lisp (SBCL) to ¶rodowisko programistyczne Open
Source dla Common Lispa oparte na CMUCL. Zawiera zintegrowany natywny
kompilator, interpreter i debugger.

%prep
%setup -q

%build
GNUMAKE="make"
CFLAGS="%{rpmcflags}"
CC="%{__cc}"
export GNUMAKE CC CFLAGS
./make.sh "sbcl --disable-debugger"
cd doc
docbook2html user-manual.sgml || :
install -d manual
mv -f *.html manual
cd ..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_mandir}/man1}

install src/runtime/sbcl $RPM_BUILD_ROOT%{_bindir}
install output/sbcl.core $RPM_BUILD_ROOT%{_libdir}
install doc/sbcl.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc BUGS COPYING CREDITS NEWS README PRINCIPLES ChangeLog doc/manual
%attr (755,root,root) %{_bindir}/sbcl
%{_libdir}/sbcl.core
%{_mandir}/man1/*

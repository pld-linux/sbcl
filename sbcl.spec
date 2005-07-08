Summary:	The Steel Bank Common Lisp development environment
Summary(pl):	¦rodowisko programowania Steel Bank Common Lisp
Name:		sbcl
Version:	0.9.0
Release:	1
License:	MIT
Group:		Development/Languages
Source0:	http://dl.sourceforge.net/sbcl/%{name}-%{version}-source.tar.bz2
# Source0-md5:	9544e79998980bfc1f555cfb900399d7
Patch0:		%{name}-home.patch
Patch1:		%{name}-gcc4.patch
URL:		http://sbcl.sourceforge.net/
BuildRequires:	sbcl
BuildRequires:	texinfo
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Steel Bank Common Lisp (SBCL) is a Open Source development environment
for Common Lisp based on CMUCL. It includes an integrated native compiler,
interpreter, and debugger.

%description -l pl
Steel Bank Common Lisp (SBCL) to ¶rodowisko programistyczne Open
Source dla Common Lispa oparte na CMUCL. Zawiera zintegrowany natywny
kompilator, interpreter i debugger.

%package doc-info
Summary:	The Steel Bank Common Lisp documentation (info)
Summary(pl):	Dokumentacja Steel Bank Common Lisp (info)
Group:		Development/Languages

%description doc-info
Documentation of Steel Bank Common Lisp (SBCL) in info format.

%description doc-info -l pl
Dokumentacja Steel Bank Common Lisp (SBCL) w formacie info.

%package doc-html
Summary:	The Steel Bank Common Lisp documentation (HTML)
Summary(pl):	Dokumentacja Steel Bank Common Lisp (HTML)
Group:		Development/Languages

%description doc-html
Documentation of Steel Bank Common Lisp (SBCL) in HTML format.

%description doc-html -l pl
Dokumentacja Steel Bank Common Lisp (SBCL) w formacie HTML.

%package doc-pdf
Summary:	The Steel Bank Common Lisp documentation (PDF)
Summary(pl):	Dokumentacja Steel Bank Common Lisp (PDF)
Group:		Development/Languages

%description doc-pdf
Documentation of Steel Bank Common Lisp (SBCL) in PDF format.

%description doc-pdf -l pl
Dokumentacja Steel Bank Common Lisp (SBCL) w formacie PDF.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
GNUMAKE="make"
CFLAGS="%{rpmcflags}"
CC="%{__cc}"
export GNUMAKE CC CFLAGS
./make.sh "sbcl --disable-debugger"
make -C doc/manual

%install
rm -rf $RPM_BUILD_ROOT
BUILD_ROOT=$RPM_BUILD_ROOT INSTALL_ROOT=%{_prefix} \
MAN_DIR=%{_mandir} INFO_DIR=%{_infodir} DOC_DIR=%{_docdir}/%{name}-%{version} \
sh ./install.sh
cp README PRINCIPLES TODO $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post doc-info
/sbin/ldconfig
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun doc-info
/sbin/ldconfig
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
%attr (755,root,root) %{_bindir}/sbcl
%{_libdir}/sbcl
%{_mandir}/man1/*
%dir %{_docdir}/%{name}-%{version}
%{_docdir}/%{name}-%{version}/BUGS
%{_docdir}/%{name}-%{version}/COPYING
%{_docdir}/%{name}-%{version}/CREDITS
%{_docdir}/%{name}-%{version}/NEWS
%{_docdir}/%{name}-%{version}/PRINCIPLES
%{_docdir}/%{name}-%{version}/README
%{_docdir}/%{name}-%{version}/SUPPORT
%{_docdir}/%{name}-%{version}/TODO

%files doc-info
%defattr(644,root,root,755)
%{_infodir}/*.info*

%files doc-html
%defattr(644,root,root,755)
%{_docdir}/%{name}-%{version}/html

%files doc-pdf
%defattr(644,root,root,755)
%{_docdir}/%{name}-%{version}/*.pdf

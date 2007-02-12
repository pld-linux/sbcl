#
# Conditional build:
%bcond_without	doc		# build without documentation
%bcond_with	clisp		# build using clisp instead of sbcl
#
# To build with an unpackaged Common Lisp implementation,
# pass --define bootstrap_cl /path/to/lisp/binary to builder.
#
Summary:	The Steel Bank Common Lisp development environment
Summary(pl.UTF-8):	Środowisko programowania Steel Bank Common Lisp
Name:		sbcl
Version:	1.0.2
Release:	1
License:	MIT
Group:		Development/Languages
Source0:	http://dl.sourceforge.net/sbcl/%{name}-%{version}-source.tar.bz2
# Source0-md5:	f94b51748e9805687759b5b924f45671
Patch0:		%{name}-home.patch
Patch1:		%{name}-threads.patch
URL:		http://sbcl.sourceforge.net/
%if %{undefined bootstrap_cl}
%if %{with clisp}
BuildRequires:	clisp
%else
BuildRequires:	sbcl
%endif
%endif
%if %{with doc}
BuildRequires:	tetex-dvips
BuildRequires:	texinfo-texi2dvi
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Steel Bank Common Lisp (SBCL) is a Open Source development environment
for Common Lisp based on CMUCL. It includes an integrated native compiler,
interpreter, and debugger.

%description -l pl.UTF-8
Steel Bank Common Lisp (SBCL) to środowisko programistyczne Open
Source dla Common Lispa oparte na CMUCL. Zawiera zintegrowany natywny
kompilator, interpreter i debugger.

%package doc-info
Summary:	The Steel Bank Common Lisp documentation (info)
Summary(pl.UTF-8):	Dokumentacja Steel Bank Common Lisp (info)
Group:		Development/Languages

%description doc-info
Documentation of Steel Bank Common Lisp (SBCL) in info format.

%description doc-info -l pl.UTF-8
Dokumentacja Steel Bank Common Lisp (SBCL) w formacie info.

%package doc-html
Summary:	The Steel Bank Common Lisp documentation (HTML)
Summary(pl.UTF-8):	Dokumentacja Steel Bank Common Lisp (HTML)
Group:		Development/Languages

%description doc-html
Documentation of Steel Bank Common Lisp (SBCL) in HTML format.

%description doc-html -l pl.UTF-8
Dokumentacja Steel Bank Common Lisp (SBCL) w formacie HTML.

%package doc-pdf
Summary:	The Steel Bank Common Lisp documentation (PDF)
Summary(pl.UTF-8):	Dokumentacja Steel Bank Common Lisp (PDF)
Group:		Development/Languages

%description doc-pdf
Documentation of Steel Bank Common Lisp (SBCL) in PDF format.

%description doc-pdf -l pl.UTF-8
Dokumentacja Steel Bank Common Lisp (SBCL) w formacie PDF.

%prep
%setup -q
%patch0 -p1
%ifarch %{ix86} %{x8664}
%patch1 -p1
%endif

%if %{undefined bootstrap_cl}
%if %{with clisp}
%define bootstrap_cl "clisp"
%else
%define bootstrap_cl "sbcl --disable-debugger"
%endif
%endif

%build
GNUMAKE="make"
CFLAGS="%{rpmcflags}"
CC="%{__cc}"
export GNUMAKE CC CFLAGS
./make.sh %{bootstrap_cl}
%if %{with doc}
make -C doc/manual
%endif

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir} $RPM_BUILD_ROOT%{_libdir} \
    $RPM_BUILD_ROOT%{_mandir} $RPM_BUILD_ROOT%{_infodir} \
    $RPM_BUILD_ROOT/etc/env.d
env -u SBCL_HOME INSTALL_ROOT=`pwd`/_install %{_buildshell} ./install.sh
mv _install/lib/sbcl $RPM_BUILD_ROOT%{_libdir}/%{name}
mv _install/bin/sbcl $RPM_BUILD_ROOT%{_bindir}/%{name}
mv _install/share/man/* $RPM_BUILD_ROOT%{_mandir}
%if %{with doc}
mv _install/share/info/*.info* $RPM_BUILD_ROOT%{_infodir}
%endif

echo SBCL_HOME=%{_libdir}/%{name} > $RPM_BUILD_ROOT/etc/env.d/SBCL_HOME

%clean
rm -rf $RPM_BUILD_ROOT

%post
%env_update

%postun
%env_update

%if %{with doc}
%post doc-info
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun doc-info
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1
%endif

%files
%defattr(644,root,root,755)
%doc _install/share/doc/sbcl/[A-Z]*
%attr (755,root,root) %{_bindir}/%{name}
%{_libdir}/%{name}
%{_mandir}/man1/*
%config(noreplace,missingok) %verify(not md5 mtime size) /etc/env.d/*

%if %{with doc}
%files doc-info
%defattr(644,root,root,755)
%{_infodir}/*.info*

%files doc-html
%defattr(644,root,root,755)
%doc _install/share/doc/sbcl/html/*

%files doc-pdf
%defattr(644,root,root,755)
%doc _install/share/doc/sbcl/*.pdf
%endif

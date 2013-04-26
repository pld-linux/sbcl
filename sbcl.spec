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
Version:	1.1.6
Release:	0.1
License:	MIT
Group:		Development/Languages
Source0:	http://download.sourceforge.net/sbcl/%{name}-%{version}-source.tar.bz2
# Source0-md5:	5daeabb9eaf7197006c4402bfc552d72
Source10:	http://download.sourceforge.net/sbcl/sbcl-1.0.58-x86-linux-binary.tar.bz2
# Source10-md5:	28104cfb0ee2ac67000c77b9518377e8
Source11:	http://download.sourceforge.net/sbcl/sbcl-1.0.58-x86-64-linux-binary.tar.bz2
# Source11-md5:	3d02edfdc851904d1d8dafeec20d1d06
Patch1:		%{name}-threads.patch
URL:		http://sbcl.sourceforge.net/
%{?with_clisp:BuildRequires:	clisp}
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
%ifarch %{ix86}
%setup -q -a 10
%endif
%ifarch %{x8664}
%setup -q -a 11
%endif
%ifarch %{ix86} %{x8664}
%patch1 -p1
%endif

mkdir sbcl-bootstrap
cd sbcl-*-linux
INSTALL_ROOT=`pwd`/../sbcl-bootstrap sh ./install.sh
cd -

# clean.sh is so stupid it removed sbcl-bootstrap contents
%{__mv} clean.sh clean.sh.orig
echo "#!/bin/sh" >clean.sh
chmod 755 clean.sh

%if %{with clisp}
%define bootstrap_cl "clisp"
%endif

%build
GNUMAKE="make"
CFLAGS="%{rpmcflags}"
CC="%{__cc}"
export GNUMAKE CC CFLAGS
export SBCL_HOME=`pwd`/sbcl-bootstrap/lib/sbcl
export PATH=`pwd`/sbcl-bootstrap/bin:${PATH}
./make.sh \
	--prefix=%{_prefix} \
	%{?bootstrap_cl}

%if %{with doc}
make -C doc/manual
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_mandir},%{_infodir}} \
	$RPM_BUILD_ROOT/etc/env.d

env -u SBCL_HOME INSTALL_ROOT=`pwd`/_install %{_buildshell} ./install.sh

%{__mv} _install/lib/sbcl $RPM_BUILD_ROOT%{_libdir}/%{name}
%{__mv} _install/bin/sbcl $RPM_BUILD_ROOT%{_bindir}/%{name}
%{__mv} _install/share/man/* $RPM_BUILD_ROOT%{_mandir}
%if %{with doc}
%{__mv} _install/share/info/*.info* $RPM_BUILD_ROOT%{_infodir}
%endif

echo SBCL_HOME=%{_libdir}/%{name} > $RPM_BUILD_ROOT/etc/env.d/SBCL_HOME

%clean
rm -rf $RPM_BUILD_ROOT

%post
%env_update

%postun
%env_update

%if %{with doc}
%post doc-info	-p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

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
%doc _install/share/doc/sbcl/*.html

%files doc-pdf
%defattr(644,root,root,755)
%doc _install/share/doc/sbcl/*.pdf
%endif

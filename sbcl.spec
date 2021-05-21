# NOTE: tests >100 processes, so ensure proper ulimit
#
# Conditional build:
%bcond_with	bootstrap	# bootstrap build
%bcond_without	doc		# build without documentation
%bcond_with	clisp		# build using clisp instead of sbcl
%bcond_without	cl_controller	# common-lisp-controller support
#
# To build with an unpackaged Common Lisp implementation,
# pass --define bootstrap_cl /path/to/lisp/binary to builder.
#
Summary:	The Steel Bank Common Lisp development environment
Summary(pl.UTF-8):	Środowisko programowania Steel Bank Common Lisp
Name:		sbcl
Version:	2.1.4
Release:	1
License:	MIT
Group:		Development/Languages
Source0:	http://download.sourceforge.net/sbcl/%{name}-%{version}-source.tar.bz2
# Source0-md5:	dab60bd97609524a69184651b1ce3d27
Source1:	sbcl.sh
Source2:	sbcl.rc
Source3:	sbcl-install-clc.lisp
Source10:	http://download.sourceforge.net/sbcl/sbcl-1.4.3-x86-linux-binary.tar.bz2
# Source10-md5:	1c022d7ac6a8154de9ae09eb9ecfc696
Source11:	http://download.sourceforge.net/sbcl/sbcl-2.1.4-x86-64-linux-binary.tar.bz2
# Source11-md5:	8d13c4827812faba6d52313860192004
Source12:	http://download.sourceforge.net/sbcl/sbcl-1.4.2-arm64-linux-binary.tar.bz2
# Source12-md5:	79a1d4624a8138564be96274707c180d
# TODO (portability) - also available:
#SourceXX:	http://download.sourceforge.net/sbcl/sbcl-1.3.9-armhf-linux-binary.tar.bz2
#SourceXX:	http://download.sourceforge.net/sbcl/sbcl-1.2.7-armel-linux-binary.tar.bz2
#SourceXX:	http://download.sourceforge.net/sbcl/sbcl-1.2.7-powerpc-linux-binary.tar.bz2
#SourceXX:	http://download.sourceforge.net/sbcl/sbcl-1.0.23-mips-linux-binary.tar.bz2
#SourceXX:	http://download.sourceforge.net/sbcl/sbcl-1.0.28-mipsel-linux-binary.tar.bz2
#SourceXX:	http://download.sourceforge.net/sbcl/sbcl-1.0.28-alpha-linux-binary.tar.bz2
#SourceXX:	http://download.sourceforge.net/sbcl/sbcl-1.0.28-sparc-linux-binary.tar.bz2
Patch0:		%{name}-tests.patch
Patch1:		%{name}-threads.patch
Patch2:		%{name}-info.patch
URL:		http://sbcl.sourceforge.net/
%{?with_clisp:BuildRequires:	clisp}
%if %{without bootstrap} && %{without clisp}
BuildRequires:	sbcl
%endif
%if %{with doc}
BuildRequires:	tetex-dvips
BuildRequires:	texinfo-texi2dvi
%endif
%if %{with cl_controller}
Requires(post,preun):	common-lisp-controller
Requires:	common-lisp-controller
%endif
%if %{without clisp}
%{?with_bootstrap:ExclusiveArch:	%{ix86} %{x8664} aarch64}
# also: %{arm} alpha mips mipsel ppc sparc
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Steel Bank Common Lisp (SBCL) is a Open Source development environment
for Common Lisp based on CMUCL. It includes an integrated native
compiler, interpreter, and debugger.

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
%if %{with bootstrap}
%ifarch %{ix86}
%setup -q -a 10
%endif
%ifarch %{x8664}
%setup -q -a 11
%endif
%ifarch aarch64
%setup -q -a 12
%endif
%else
%setup -q
%endif
%patch0 -p1
%ifarch %{ix86} %{x8664}
%patch1 -p1
%endif
%patch2 -p1

%if %{with bootstrap}
mkdir sbcl-bootstrap
cd sbcl-*-linux
INSTALL_ROOT=`pwd`/../sbcl-bootstrap sh ./install.sh
cd -
%endif

# clean.sh is so stupid it removed sbcl-bootstrap contents
%{__mv} clean.sh clean.sh.orig
echo "#!/bin/sh" >clean.sh
chmod 755 clean.sh

%if %{with clisp}
%define bootstrap_cl clisp
%endif

%build
export GNUMAKE="make"
export SBCL_MAKE_JOBS="%{_smp_mflags}"
export CC="%{__cc}"
export CFLAGS="%{rpmcflags}"
export CPPFLAGS="%{rpmcppflags}"
export LDFLAGS="%{rpmldflags}"
%if %{with bootstrap}
export SBCL_HOME=`pwd`/sbcl-bootstrap/lib/sbcl
export PATH=`pwd`/sbcl-bootstrap/bin:${PATH}
%endif
%{__sed} -i -e 's/^CFLAGS/#CFLAGS/' src/runtime/GNUmakefile
./make.sh \
	--prefix=%{_prefix} \
	%{?bootstrap_cl:--xc-host=%{bootstrap_cl}}

%if %{with doc}
%{__make} -C doc/manual -j1
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

%if %{with cl_controller}
install -d $RPM_BUILD_ROOT{/usr/lib/common-lisp/bin,%{_sysconfdir}}
%{__sed} -e 's,/usr/lib/sbcl,%{_libdir}/%{name},g' %{SOURCE1} >$RPM_BUILD_ROOT/usr/lib/common-lisp/bin/sbcl.sh
install -Dp %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sbcl.rc
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_libdir}/%{name}/install-clc.lisp
%{__mv} $RPM_BUILD_ROOT%{_libdir}/%{name}/sbcl.core $RPM_BUILD_ROOT%{_libdir}/%{name}/sbcl-dist.core
touch $RPM_BUILD_ROOT%{_libdir}/%{name}/sbcl.core
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%env_update
%if %{with cl_controller}
test -f %{_libdir}/%{name}/sbcl.core || cp -p %{_libdir}/%{name}/sbcl-dist.core %{_libdir}/%{name}/sbcl.core
/usr/sbin/register-common-lisp-implementation sbcl >/dev/null 2>&1 ||:
%endif

%postun
%env_update

%if %{with cl_controller}
if [ $1 -eq 0 ]; then
	/usr/sbin/unregister-common-lisp-implementation sbcl >/dev/null 2>&1 ||:
fi
%endif

%if %{with doc}
%post doc-info	-p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun doc-info
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1
%endif

%files
%defattr(644,root,root,755)
%doc _install/share/doc/sbcl/{BUGS,COPYING,CREDITS,NEWS}
%attr (755,root,root) %{_bindir}/sbcl
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/contrib
%{_mandir}/man1/sbcl.1*
%config(noreplace,missingok) %verify(not md5 mtime size) /etc/env.d/SBCL_HOME
%if %{with cl_controller}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/sbcl.rc
%attr(744,root,root) /usr/lib/common-lisp/bin/sbcl.sh
%{_libdir}/%{name}/install-clc.lisp
%{_libdir}/%{name}/sbcl-dist.core
%{_libdir}/%{name}/sbcl.mk
%ghost %{_libdir}/%{name}/sbcl.core
%else
%{_libdir}/%{name}/sbcl.core
%endif

%if %{with doc}
%files doc-info
%defattr(644,root,root,755)
%{_infodir}/asdf.info*
%{_infodir}/sbcl.info*

%files doc-html
%defattr(644,root,root,755)
%doc _install/share/doc/sbcl/*.html

%files doc-pdf
%defattr(644,root,root,755)
%doc _install/share/doc/sbcl/*.pdf
%endif

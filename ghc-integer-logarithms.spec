#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	integer-logarithms
Summary:	Integer logarithms
Name:		ghc-%{pkgname}
Version:	1.0.3
Release:	2
License:	MIT
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/integer-logarithms
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	123bd756df01fd700bde26991f8431df
Patch0:		ghc-8.10.patch
URL:		http://hackage.haskell.org/package/integer-logarithms
BuildRequires:	ghc >= 6.12.3
%if %{with prof}
BuildRequires:	ghc-prof
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires(post,postun):	/usr/bin/ghc-pkg
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
Math.NumberTheory.Logarithms and Math.NumberTheory.Powers.Integer
from the arithmoi package.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-prof

%description prof
Profiling %{pkgname} library for GHC.  Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
%ifarch x32
	--flags="-integer-gmp" \
%endif
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc LICENSE changelog.md readme.md %{name}-%{version}-doc/html
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a

%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/GHC
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/GHC/Integer
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/GHC/Integer/Logarithms
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/GHC/Integer/Logarithms/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/GHC/Integer/Logarithms/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Math/
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Math/NumberTheory
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Math/NumberTheory/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Math/NumberTheory/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Math/NumberTheory/Powers
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Math/NumberTheory/Powers/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Math/NumberTheory/Powers/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/GHC/Integer/Logarithms/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Math/NumberTheory/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Math/NumberTheory/Powers/*.p_hi
%endif

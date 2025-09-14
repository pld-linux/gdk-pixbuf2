# NOTE: as of 2.44.1, glycin works only as builtin
#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	glycin		# Glycin loaders support
%bcond_without	tests		# test suite

%define		abiver		2.10.0
Summary:	GdkPixbuf - an image loading and scaling library
Summary(pl.UTF-8):	GdkPixbuf - biblioteka ładująca i skalująca obrazki
Name:		gdk-pixbuf2
Version:	2.44.1
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	https://download.gnome.org/sources/gdk-pixbuf/2.44/gdk-pixbuf-%{version}.tar.xz
# Source0-md5:	27c04b847fcf9e5bfb7ac5ce2a08ecd0
URL:		https://developer.gnome.org/gdk-pixbuf/
BuildRequires:	docutils
BuildRequires:	gettext-tools >= 0.19
BuildRequires:	glib2-devel >= 1:2.56.0
%{?with_glycin:BuildRequires:	glycin-devel >= 2.0}
%{?with_tests:BuildRequires:	glycin-loaders >= 2.0}
BuildRequires:	gobject-introspection-devel >= 0.10.0
%{?with_apidocs:BuildRequires:	gi-docgen >= 2021.1}
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel >= 1.0
BuildRequires:	libtiff-devel >= 4
BuildRequires:	meson >= 1.5
BuildRequires:	ninja >= 1.5
BuildRequires:	perl-devel
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.042
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	glib2 >= 1:2.56.0
%if %{with glycin}
Requires:	glycin-loaders >= 2.0
Requires:	glycin-thumbnailer >= 2.0
%endif
Requires:	shared-mime-info
Suggests:	librsvg >= 2.31
Conflicts:	gtk+2 < 2:2.21.3-1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%if "%{_lib}" != "lib"
%define		libext		%(lib="%{_lib}"; echo ${lib#lib})
%define		pqext		-%{libext}
%else
%define		pqext		%{nil}
%endif

%description
gdk-pixbuf is an image loading and scaling library that can be
extended by loadable modules for new image formats.

It is used by toolkits such as GTK+ or Clutter.

%description -l pl.UTF-8
gdk-pixbuf to biblioteka ładująca i skalująca obrazki, której
funkcjonalność może być rozszerzana o obsługę nowych formatów poprzez
ładowane moduły.

Używana jest przez biblioteki takie jak GTK+ czy Clutter.

%package devel
Summary:	Header files for gdk-pixbuf library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki gdk-pixbuf
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.56.0
%{?with_glycin:Requires:	glycin-devel >= 2.0}
Requires:	libjpeg-devel
Requires:	libpng-devel >= 1.0
Requires:	libtiff-devel >= 4
Conflicts:	gtk+2-devel < 2:2.21.3-1

%description devel
Header files for gdk-pixbuf library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki gdk-pixbuf.

%package static
Summary:	Static gdk-pixbuf library
Summary(pl.UTF-8):	Biblioteka statyczna gdk-pixbuf
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static gdk-pixbuf library.

%description static -l pl.UTF-8
Biblioteka statyczna gdk-pixbuf.

%package apidocs
Summary:	gdk-pixbuf API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki gdk-pixbuf
Group:		Documentation
Conflicts:	gtk+2-apidocs < 2:2.21.3-1
BuildArch:	noarch

%description apidocs
API documentation for gdk-pixbuf library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki gdk-pixbuf.

%prep
%setup -q -n gdk-pixbuf-%{version}

%build
%meson \
	-Dandroid=disabled \
	-Dbuiltin_loaders=%{?with_glycin:glycin} \
	-Ddocumentation=true \
	-Dgif=enabled \
	%{?with_apidocs:-Dgtk_doc=true} \
	-Dglycin=%{__enabled_disabled glycin} \
	-Dinstalled_tests=false \
	-Dintrospection=enabled \
	-Djpeg=enabled \
	-Dothers=enabled \
	-Dpng=enabled \
	-Dthumbnailer=enabled \
	%{!?with_tests:-Dtests=false} \
	-Dtiff=enabled

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

%if "%{_lib}" != "lib"
# We need to have 32-bit and 64-bit binaries as they have hardcoded LIBDIR.
# (needed when multilib is used)
%{__mv} $RPM_BUILD_ROOT%{_bindir}/gdk-pixbuf-query-loaders{,%{pqext}}
%{__sed} -i -e 's,gdk-pixbuf-query-loaders$,&%{pqext},' $RPM_BUILD_ROOT%{_pkgconfigdir}/gdk-pixbuf-2.0.pc
%endif

%if %{with apidocs}
install -d $RPM_BUILD_ROOT%{_gidocdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/gdk-* $RPM_BUILD_ROOT%{_gidocdir}
%endif

touch $RPM_BUILD_ROOT%{_libdir}/gdk-pixbuf-2.0/%{abiver}/loaders.cache

%{__mv} $RPM_BUILD_ROOT%{_localedir}/{sr@ije,sr@ijekavian}
# not supported by glibc
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/io

%find_lang gdk-pixbuf %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
umask 022
%{_bindir}/gdk-pixbuf-query-loaders%{pqext} --update-cache || :

%postun
/sbin/ldconfig
if [ "$1" != "0" ]; then
	umask 022
	# the $1 check does not match for multilib installs, check also that the binary still exists
	[ ! -x %{_bindir}/gdk-pixbuf-query-loaders%{pqext} ] || \
	%{_bindir}/gdk-pixbuf-query-loaders%{pqext} --update-cache || :
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc NEWS README.md
%attr(755,root,root) %{_bindir}/gdk-pixbuf-query-loaders%{pqext}
%attr(755,root,root) %{_bindir}/gdk-pixbuf-thumbnailer
%attr(755,root,root) %{_libdir}/libgdk_pixbuf-2.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgdk_pixbuf-2.0.so.0
%dir %{_libdir}/gdk-pixbuf-2.0
%dir %{_libdir}/gdk-pixbuf-2.0/%{abiver}
%ghost %{_libdir}/gdk-pixbuf-2.0/%{abiver}/loaders.cache
%dir %{_libdir}/gdk-pixbuf-2.0/%{abiver}/loaders
%attr(755,root,root) %{_libdir}/gdk-pixbuf-2.0/%{abiver}/loaders/libpixbufloader-ani.so
%attr(755,root,root) %{_libdir}/gdk-pixbuf-2.0/%{abiver}/loaders/libpixbufloader-bmp.so
%attr(755,root,root) %{_libdir}/gdk-pixbuf-2.0/%{abiver}/loaders/libpixbufloader-gif.so
%attr(755,root,root) %{_libdir}/gdk-pixbuf-2.0/%{abiver}/loaders/libpixbufloader-icns.so
%attr(755,root,root) %{_libdir}/gdk-pixbuf-2.0/%{abiver}/loaders/libpixbufloader-ico.so
%attr(755,root,root) %{_libdir}/gdk-pixbuf-2.0/%{abiver}/loaders/libpixbufloader-jpeg.so
%attr(755,root,root) %{_libdir}/gdk-pixbuf-2.0/%{abiver}/loaders/libpixbufloader-png.so
%attr(755,root,root) %{_libdir}/gdk-pixbuf-2.0/%{abiver}/loaders/libpixbufloader-pnm.so
%attr(755,root,root) %{_libdir}/gdk-pixbuf-2.0/%{abiver}/loaders/libpixbufloader-qtif.so
%attr(755,root,root) %{_libdir}/gdk-pixbuf-2.0/%{abiver}/loaders/libpixbufloader-tga.so
%attr(755,root,root) %{_libdir}/gdk-pixbuf-2.0/%{abiver}/loaders/libpixbufloader-tiff.so
%attr(755,root,root) %{_libdir}/gdk-pixbuf-2.0/%{abiver}/loaders/libpixbufloader-xbm.so
%attr(755,root,root) %{_libdir}/gdk-pixbuf-2.0/%{abiver}/loaders/libpixbufloader-xpm.so
%{_datadir}/thumbnailers/gdk-pixbuf-thumbnailer.thumbnailer
%{_libdir}/girepository-1.0/GdkPixbuf-2.0.typelib
%{_libdir}/girepository-1.0/GdkPixdata-2.0.typelib
%{_mandir}/man1/gdk-pixbuf-query-loaders.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gdk-pixbuf-csource
%attr(755,root,root) %{_bindir}/gdk-pixbuf-pixdata
%attr(755,root,root) %{_libdir}/libgdk_pixbuf-2.0.so
%{_datadir}/gir-1.0/GdkPixbuf-2.0.gir
%{_datadir}/gir-1.0/GdkPixdata-2.0.gir
%{_mandir}/man1/gdk-pixbuf-csource.1*
%{_includedir}/gdk-pixbuf-2.0
%{_pkgconfigdir}/gdk-pixbuf-2.0.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libgdk_pixbuf-2.0.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gidocdir}/gdk-pixbuf
%{_gidocdir}/gdk-pixdata
%endif

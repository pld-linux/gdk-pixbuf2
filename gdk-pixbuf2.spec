# TODO: consider -x11 subpackages
#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs

%define		abiver		2.10.0
Summary:	An image loading and scaling library
Summary(pl.UTF-8):	Biblioteka ładująca i skalująca obrazki
Name:		gdk-pixbuf2
Version:	2.38.2
Release:	1
License:	LGPL v2+
Group:		X11/Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gdk-pixbuf/2.38/gdk-pixbuf-%{version}.tar.xz
# Source0-md5:	cc1d712a1643b92ff0904d589963971f
URL:		https://developer.gnome.org/gdk-pixbuf/
BuildRequires:	docbook-dtd43-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	gettext-tools >= 0.19
BuildRequires:	glib2-devel >= 1:2.48.0
BuildRequires:	gobject-introspection-devel >= 0.10.0
BuildRequires:	gtk-doc >= 1.20
BuildRequires:	jasper-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel >= 1.0
BuildRequires:	libtiff-devel >= 4
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	libxslt-progs
BuildRequires:	meson >= 0.46.0
BuildRequires:	ninja
BuildRequires:	perl-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.727
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xz
Requires:	glib2 >= 1:2.48.0
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
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.48.0
Conflicts:	gtk+2-devel < 2:2.21.3-1
# for gdk-pixbuf-xlib-2.0:
Requires:	xorg-lib-libX11-devel

%description devel
Header files for gdk-pixbuf library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki gdk-pixbuf.

%package static
Summary:	Static gdk-pixbuf libraries
Summary(pl.UTF-8):	Biblioteki statyczne gdk-pixbuf
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static gdk-pixbuf libraries.

%description static -l pl.UTF-8
Biblioteki statyczne gdk-pixbuf.

%package apidocs
Summary:	gdk-pixbuf API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki gdk-pixbuf
Group:		Documentation
Conflicts:	gtk+2-apidocs < 2:2.21.3-1
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for gdk-pixbuf library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki gdk-pixbuf.

%prep
%setup -q -n gdk-pixbuf-%{version}

%build
%meson build \
	-Ddocs=%{?with_apidocs:true}%{!?with_apidocs:false} \
	-Dinstalled_tests=false \
	-Djasper=true \
	-Dman=true \
	-Dx11=true
%meson_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install -j1 -C build

%if "%{_lib}" != "lib"
# We need to have 32-bit and 64-bit binaries as they have hardcoded LIBDIR.
# (needed when multilib is used)
%{__mv} $RPM_BUILD_ROOT%{_bindir}/gdk-pixbuf-query-loaders{,%{pqext}}
%endif

touch $RPM_BUILD_ROOT%{_libdir}/gdk-pixbuf-2.0/%{abiver}/loaders.cache

%{!?with_apidocs:%{__rm} -r $RPM_BUILD_ROOT%{_gtkdocdir}}

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
%attr(755,root,root) %{_libdir}/libgdk_pixbuf_xlib-2.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgdk_pixbuf_xlib-2.0.so.0
%dir %{_libdir}/gdk-pixbuf-2.0
%dir %{_libdir}/gdk-pixbuf-2.0/%{abiver}
%ghost %{_libdir}/gdk-pixbuf-2.0/%{abiver}/loaders.cache
%dir %{_libdir}/gdk-pixbuf-2.0/%{abiver}/loaders
%attr(755,root,root) %{_libdir}/gdk-pixbuf-2.0/%{abiver}/loaders/libpixbufloader-*.so
%{_datadir}/thumbnailers/gdk-pixbuf-thumbnailer.thumbnailer
%{_libdir}/girepository-1.0/GdkPixbuf-2.0.typelib
%{_libdir}/girepository-1.0/GdkPixdata-2.0.typelib
%{_mandir}/man1/gdk-pixbuf-query-loaders.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gdk-pixbuf-csource
%attr(755,root,root) %{_bindir}/gdk-pixbuf-pixdata
%attr(755,root,root) %{_libdir}/libgdk_pixbuf-2.0.so
%attr(755,root,root) %{_libdir}/libgdk_pixbuf_xlib-2.0.so
%{_datadir}/gir-1.0/GdkPixbuf-2.0.gir
%{_datadir}/gir-1.0/GdkPixdata-2.0.gir
%{_mandir}/man1/gdk-pixbuf-csource.1*
%{_includedir}/gdk-pixbuf-2.0
%{_pkgconfigdir}/gdk-pixbuf-2.0.pc
%{_pkgconfigdir}/gdk-pixbuf-xlib-2.0.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libgdk_pixbuf-2.0.a
%{_libdir}/libgdk_pixbuf_xlib-2.0.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gdk-pixbuf
%endif

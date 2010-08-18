#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
#
%define		abiver		2.10.0
#
Summary:	An image loading library
Summary(pl.UTF-8):	Biblioteka ładująca obrazki
Name:		gdk-pixbuf2
Version:	2.21.6
Release:	1
License:	LGPL v2
Group:		X11/Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gdk-pixbuf/2.21/gdk-pixbuf-%{version}.tar.bz2
# Source0-md5:	03b8b833e376b72dd228e268ff8fe733
URL:		http://www.gtk.org/
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.10
BuildRequires:	gettext-devel >= 0.17
BuildRequires:	glib2-devel >= 1:2.25.9
BuildRequires:	gobject-introspection-devel >= 0.6.14
BuildRequires:	gtk-doc >= 1.11
BuildRequires:	jasper-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	libxslt-progs
BuildRequires:	perl-devel
BuildRequires:	pkgconfig
BuildRequires:	xorg-lib-libX11-devel
Requires:	glib2 >= 1:2.25.9
Conflicts:	gtk+2 < 2:2.21.3-1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%if "%{_lib}" != "lib"
%define		libext		%(lib="%{_lib}"; echo ${lib#lib})
%define		pqext		-%{libext}
%else
%define		pqext		%{nil}
%endif

%description
gdk-pixbuf is an image loading library that can be extended by
loadable modules for new image formats.

It is used by toolkits such as GTK+ or Clutter.

%description -l pl.UTF-8
gdk-pixbuf to biblioteka ładująca obrazki, której funkcjonalność może
być rozszerzana o obsługę nowych formatów poprzez ładowane moduły.

Używana jest przez biblioteki takie jak GTK+ czy Clutter.

%package devel
Summary:	Header files for gdk-pixbuf library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki gdk-pixbuf
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.25.9
Conflicts:	gtk+2-devel < 2:2.21.3-1

%description devel
Header files for gdk-pixbuf library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki gdk-pixbuf.

%package apidocs
Summary:	gdk-pixbuf API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki gdk-pixbuf
Group:		Documentation
Conflicts:	gtk+2-apidocs < 2:2.21.3-1

%description apidocs
API documentation for gdk-pixbuf library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki gdk-pixbuf.

%prep
%setup -q -n gdk-pixbuf-%{version}
sed -i s#^io## po/LINGUAS
rm po/io.po

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-man \
	%{__enable_disable apidocs gtk-doc} \
	--with-html-dir=%{_gtkdocdir} \
	--with-libjasper
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if "%{_lib}" != "lib"
# We need to have 32-bit and 64-bit binaries as they have hardcoded LIBDIR.
# (needed when multilib is used)
%{__mv} $RPM_BUILD_ROOT%{_bindir}/gdk-pixbuf-query-loaders{,%{pqext}}
%endif

touch $RPM_BUILD_ROOT%{_libdir}/gdk-pixbuf-2.0/%{abiver}/loaders.cache

%{__rm} -f $RPM_BUILD_ROOT%{_libdir}/gdk-pixbuf-2.0/%{abiver}/loaders/*.la

%{?!with_apidocs:%{__rm} -rf $RPM_BUILD_ROOT%{_gtkdocdir}}

%find_lang gdk-pixbuf

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

umask 022
%{_bindir}/gdk-pixbuf-query-loaders%{pqext} --update-cache
exit 0

%postun
/sbin/ldconfig

if [ "$1" != "0" ]; then
    umask 022
    %{_bindir}/gdk-pixbuf-query-loaders%{pqext} --update-cache
fi
exit 0

%files -f gdk-pixbuf.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS
%attr(755,root,root) %{_bindir}/gdk-pixbuf-query-loaders%{pqext}
%attr(755,root,root) %{_libdir}/libgdk_pixbuf-2.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgdk_pixbuf-2.0.so.0
%attr(755,root,root) %{_libdir}/libgdk_pixbuf_xlib-2.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgdk_pixbuf_xlib-2.0.so.0
%dir %{_libdir}/gdk-pixbuf-2.0
%dir %{_libdir}/gdk-pixbuf-2.0/%{abiver}
%ghost %{_libdir}/gdk-pixbuf-2.0/%{abiver}/loaders.cache
%dir %{_libdir}/gdk-pixbuf-2.0/%{abiver}/loaders
%{_libdir}/gdk-pixbuf-2.0/%{abiver}/loaders/libpixbufloader-ani.so
%{_libdir}/gdk-pixbuf-2.0/%{abiver}/loaders/libpixbufloader-bmp.so
%{_libdir}/gdk-pixbuf-2.0/%{abiver}/loaders/libpixbufloader-gif.so
%{_libdir}/gdk-pixbuf-2.0/%{abiver}/loaders/libpixbufloader-icns.so
%{_libdir}/gdk-pixbuf-2.0/%{abiver}/loaders/libpixbufloader-ico.so
%{_libdir}/gdk-pixbuf-2.0/%{abiver}/loaders/libpixbufloader-jasper.so
%{_libdir}/gdk-pixbuf-2.0/%{abiver}/loaders/libpixbufloader-jpeg.so
%{_libdir}/gdk-pixbuf-2.0/%{abiver}/loaders/libpixbufloader-pcx.so
%{_libdir}/gdk-pixbuf-2.0/%{abiver}/loaders/libpixbufloader-png.so
%{_libdir}/gdk-pixbuf-2.0/%{abiver}/loaders/libpixbufloader-pnm.so
%{_libdir}/gdk-pixbuf-2.0/%{abiver}/loaders/libpixbufloader-qtif.so
%{_libdir}/gdk-pixbuf-2.0/%{abiver}/loaders/libpixbufloader-ras.so
%{_libdir}/gdk-pixbuf-2.0/%{abiver}/loaders/libpixbufloader-tga.so
%{_libdir}/gdk-pixbuf-2.0/%{abiver}/loaders/libpixbufloader-tiff.so
%{_libdir}/gdk-pixbuf-2.0/%{abiver}/loaders/libpixbufloader-wbmp.so
%{_libdir}/gdk-pixbuf-2.0/%{abiver}/loaders/libpixbufloader-xbm.so
%{_libdir}/gdk-pixbuf-2.0/%{abiver}/loaders/libpixbufloader-xpm.so
%{_libdir}/girepository-1.0/GdkPixbuf-2.0.typelib
%{_mandir}/man1/gdk-pixbuf-query-loaders.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gdk-pixbuf-csource
%attr(755,root,root) %{_libdir}/libgdk_pixbuf-2.0.so
%attr(755,root,root) %{_libdir}/libgdk_pixbuf_xlib-2.0.so
%{_libdir}/libgdk_pixbuf-2.0.la
%{_libdir}/libgdk_pixbuf_xlib-2.0.la
%{_datadir}/gir-1.0/GdkPixbuf-2.0.gir
%{_mandir}/man1/gdk-pixbuf-csource.1*
%{_includedir}/gdk-pixbuf-2.0
%{_pkgconfigdir}/gdk-pixbuf-2.0.pc
%{_pkgconfigdir}/gdk-pixbuf-xlib-2.0.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gdk-pixbuf
%endif

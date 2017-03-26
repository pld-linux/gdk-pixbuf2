# TODO: consider -x11 subpackages
#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs

%define		abiver		2.10.0
Summary:	An image loading and scaling library
Summary(pl.UTF-8):	Biblioteka ładująca i skalująca obrazki
Name:		gdk-pixbuf2
Version:	2.36.6
Release:	1
License:	LGPL v2+
Group:		X11/Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gdk-pixbuf/2.36/gdk-pixbuf-%{version}.tar.xz
# Source0-md5:	5dd53760750670d27c194ff6ace7eb51
Patch0:		%{name}-png-nodep.patch
URL:		https://developer.gnome.org/gdk-pixbuf/
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
BuildRequires:	docbook-dtd43-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	gettext-tools >= 0.19
BuildRequires:	glib2-devel >= 1:2.37.6
BuildRequires:	gobject-introspection-devel >= 0.10.0
BuildRequires:	gtk-doc >= 1.20
BuildRequires:	jasper-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	libxslt-progs
BuildRequires:	perl-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.527
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xz
Requires:	glib2 >= 1:2.37.6
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
Requires:	glib2-devel >= 1:2.37.6
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
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for gdk-pixbuf library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki gdk-pixbuf.

%prep
%setup -q -n gdk-pixbuf-%{version}
%patch0 -p1

%build
%{__gettextize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--enable-man \
	%{__enable_disable apidocs gtk-doc} \
	--with-html-dir=%{_gtkdocdir} \
	--with-libjasper \
	--with-x11
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if "%{_lib}" != "lib"
# We need to have 32-bit and 64-bit binaries as they have hardcoded LIBDIR.
# (needed when multilib is used)
mv -f $RPM_BUILD_ROOT%{_bindir}/gdk-pixbuf-query-loaders{,%{pqext}}
%endif

touch $RPM_BUILD_ROOT%{_libdir}/gdk-pixbuf-2.0/%{abiver}/loaders.cache

%{__rm} $RPM_BUILD_ROOT%{_libdir}/gdk-pixbuf-2.0/%{abiver}/loaders/*.la \
	$RPM_BUILD_ROOT%{_libdir}/libgdk_pixbuf{,_xlib}-2.0.la

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
%doc AUTHORS NEWS
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
%{_mandir}/man1/gdk-pixbuf-query-loaders.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gdk-pixbuf-csource
%attr(755,root,root) %{_bindir}/gdk-pixbuf-pixdata
%attr(755,root,root) %{_libdir}/libgdk_pixbuf-2.0.so
%attr(755,root,root) %{_libdir}/libgdk_pixbuf_xlib-2.0.so
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

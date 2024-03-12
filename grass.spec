%if %{_use_internal_dependency_generator}
%define __noautoreq '(.*)\\.so$|(.*)\\.so\\(\\)\\(64bit\\)$'
%define __noautoprov '(.*)\\.so$|(.*)\\.so\\(\\)\\(64bit\\)$'
%endif

%define short_ver %(echo %{version}|cut -d. -f 1,2 | sed -e 's/\\.//g')

Name:		grass
Version:	8.3.2
Release:	1
Group:		Sciences/Geosciences
Summary:	Geographic Resources Analysis Support System
License:	GPLv2+
URL:		http://grass.osgeo.org/

Source:		https://github.com/OSGeo/grass/archive/refs/tags/%{version}/%{name}-%{version}.tar.gz
Source2:	grass5_48.png
Source3:	grass5_32.png
Source4:	grass5_16.png

Patch0:		grass-8.3.0-mariadb-fix-build.patch

BuildRequires:	bison
BuildRequires:	gcc-gfortran
BuildRequires:	flex
BuildRequires:	swig
BuildRequires:	gd-devel >= 2.0
BuildRequires:	gdal-devel
BuildRequires:	gdbm-devel
BuildRequires:	gettext
BuildRequires:	jpeg-devel
BuildRequires:	mysql-devel
BuildRequires:	postgresql-devel
BuildRequires:	proj proj-devel
BuildRequires:	readline-devel
BuildRequires:	tiff-devel
BuildRequires:	unixODBC-devel

BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(cfitsio)
BuildRequires:	pkgconfig(fftw3)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(geos)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(xmu)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(pdal)
BuildRequires:  python-wxpython

# disabled ffmpeg support for now, since it has to be fixed upstream
#BuildRequires:	ffmpeg-devel

Requires:	python-wxpython

%description
GRASS (Geographic Resources Analysis Support System) is an 
open source, Free Software Geographical Information System (GIS)
with raster, topological vector, image processing, and graphics
production functionality that operates on various platforms 
through a graphical user interface and shell in X-Window.

%prep
%autosetup -p1

%build
#autoreconf -fi
%define __cputoolize true
%define Werror_cflags %nil
%configure --host=%{_host} \
	--with-postgres \
	--with-postgres-includes=%{_includedir}/ \
	--with-freetype \
	--with-freetype-includes=%{_includedir}/freetype2 \
	--with-cairo \
	--with-opengl-libs=%{_libdir} \
	--with-gdal  \
        --with-geos \
	--with-mysql --with-mysql-includes=%{_includedir}/mysql \
	--with-odbc \
	--enable-largefile \
	--with-sqlite \
	--with-cxx \
	--with-proj-share=%{_datadir}/proj \
	--with-nls \
	--with-readline \
#   --with-ffmpeg --with-ffmpeg-includes="%{_includedir}/libavcodec \
#   %{_includedir}/libavdevice \
#   %{_includedir}/libavformat %{_includedir}/libavutil \
#   %{_includedir}/libpostproc %{_includedir}/libswscale"

%make_build

%install

%make_install \
	DESTDIR=%{buildroot} \
	prefix=%{_libdir} \
	UNIX_BIN=%{_bindir} 

mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps

install -m644 %{SOURCE2} %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
install -m644 %{SOURCE3} %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -m644 %{SOURCE4} %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Grass
Comment=Geographic Resources Analysis Support System
Exec=grass
Icon=%{name}
Terminal=true
Type=Application
Categories=Science;Geology;
EOF

mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d
cat > %{buildroot}%{_sysconfdir}/ld.so.conf.d/grass.conf << EOF
%{_libdir}/grass%{short_ver}/lib
EOF

%files
%attr(0755,root,root) %{_bindir}/*
%{_sysconfdir}/ld.so.conf.d/*
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/*/*/*/*
%{_libdir}/grass%{short_ver}/{AUTHORS,CHANGES,CITING,COPYING,GPL.txt,GPL.TXT,INSTALL.md,REQUIREMENTS.md,REQUIREMENTS.html}
%{_libdir}/grass%{short_ver}/bin
%{_libdir}/grass%{short_ver}/contributors*
%{_libdir}/grass%{short_ver}/demolocation
%{_libdir}/grass%{short_ver}/docs
%{_libdir}/grass%{short_ver}/driver
%{_libdir}/grass%{short_ver}/etc
%{_libdir}/grass%{short_ver}/fonts
%{_libdir}/grass%{short_ver}/gui
%{_libdir}/grass%{short_ver}/include
%{_libdir}/grass%{short_ver}/lib
%{_libdir}/grass%{short_ver}/locale
%{_libdir}/grass%{short_ver}/scripts
%{_libdir}/grass%{short_ver}/share
%{_libdir}/grass%{short_ver}/translat*
%{_libdir}/grass%{short_ver}/utils

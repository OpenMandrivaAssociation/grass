%define grassfix 64

%if %{_use_internal_dependency_generator}
%define __noautoreq '(.*)\\.so$|(.*)\\.so\\(\\)\\(64bit\\)$'
%define __noautoprov '(.*)\\.so$|(.*)\\.so\\(\\)\\(64bit\\)$'
%endif

Name:		grass
Version:	6.4.2
Release:	3
Group:		Sciences/Geosciences
Summary:	Geographic Resources Analysis Support System
License:	GPLv2+
URL:		http://grass.osgeo.org/

Source:		http://grass.osgeo.org/grass%{grassfix}/source/grass-%{version}.tar.gz
Source2:	grass5_48.png
Source3:	grass5_32.png
Source4:	grass5_16.png
Patch0:		grass-6.4.2-upstream-fix-gcc4_7.patch
Patch1:		grass-6.4.2-nopycompile.patch
Patch2:		grass-6.4.2-tk8.6.patch
Patch3:		grass-6.4.2-docfiles.patch

BuildRequires:	bison
BuildRequires:	gcc-gfortran
BuildRequires:	flex
BuildRequires:	lzma
BuildRequires:	swig
BuildRequires:	gd-devel >= 2.0
BuildRequires:	gdal-devel
BuildRequires:	gdbm-devel
BuildRequires:	jpeg-devel
BuildRequires:	lesstif-devel
BuildRequires:	mysql-devel
BuildRequires:	postgresql-devel
BuildRequires:	proj proj-devel
BuildRequires:	readline-devel
BuildRequires:	tcl tcl-devel
BuildRequires:	termcap-devel
BuildRequires:	tiff-devel
BuildRequires:	tk tk-devel
BuildRequires:	unixODBC-devel
BuildRequires:	wxgtku-devel
BuildRequires:	wxPythonGTK-devel

BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(cfitsio)
BuildRequires:	pkgconfig(fftw3)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(xmu)
BuildRequires:	pkgconfig(zlib)

# disabled ffmpeg support for now, since it has to be fixed upstream
#BuildRequires:	ffmpeg-devel

Requires:	xterm
Requires:	tk
Requires:	tcl

%description
GRASS (Geographic Resources Analysis Support System) is an 
open source, Free Software Geographical Information System (GIS)
with raster, topological vector, image processing, and graphics
production functionality that operates on various platforms 
through a graphical user interface and shell in X-Window.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
#autoreconf -fi
%define __cputoolize true
%define Werror_cflags %nil
%configure2_5x --host=%{_host} \
%if "%_lib" != "lib"
	--enable-64bit \
%endif
	--with-dbm-includes=%{_includedir}/gdbm/ \
	--with-postgres \
	--with-postgres-includes=%{_includedir}/ \
	--with-freetype \
	--with-freetype-includes=%{_includedir}/freetype2 \
	--with-motif \
	--with-cairo \
	--with-opengl-libs=%{_libdir} \
	--with-motif-libs=%{_libdir} \
	--with-motif-libs=%{_libdir} \
	--with-motif-includes=%{_includedir} \
	--with-gdal  \
        --with-geos \
	--with-mysql --with-mysql-includes=%{_includedir}/mysql \
	--with-odbc \
	--enable-largefile \
	--with-curses \
	--with-python --with-wxwidgets="%{_bindir}/wx-config"\
	--with-sqlite \
	--with-cxx \
	--with-proj-share=%{_datadir}/proj \
	--with-nls \
	--with-readline \
#   --with-ffmpeg --with-ffmpeg-includes="%{_includedir}/libavcodec \
#   %{_includedir}/libavdevice \
#   %{_includedir}/libavformat %{_includedir}/libavutil \
#   %{_includedir}/libpostproc %{_includedir}/libswscale"

%make

%install
mkdir -p %{buildroot}/%{_bindir}
#%makeinstall_std INST_DIR=%{_libdir}/grass%{grassfix}
# Actions in make install that don't take into account packaging in a place different to running:
sed -e 's|^GISBASE.*|GISBASE=%{_libdir}/grass%{grassfix}|' \
 bin.%{_target_platform}/grass%{grassfix} > %{buildroot}/%{_bindir}/grass%{grassfix}
chmod a+x %{buildroot}/usr/bin/grass%{grassfix}

mkdir -p %{buildroot}/%{_libdir}/grass%{grassfix}
cp -a dist.%{_target_platform}/* %{buildroot}/%{_libdir}/grass%{grassfix}

# Add makefiles to includes:
cp -a include/Make %{buildroot}/%{_libdir}/grass%{grassfix}/include/

# Manually archive the man pages:
lzma %{buildroot}/%{_libdir}/grass%{grassfix}/man/man?/*

mkdir %{buildroot}/%{_libdir}/grass%{grassfix}/locks/

mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps

install -m644 %{SOURCE2} %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
install -m644 %{SOURCE3} %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -m644 %{SOURCE4} %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Grass%{grassfix}
Comment=Geographic Resources Analysis Support System
Exec=grass%{grassfix}
Icon=%{name}
Terminal=true
Type=Application
Categories=Science;Geology;
EOF

mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d
cat > %{buildroot}%{_sysconfdir}/ld.so.conf.d/grass.conf << EOF
%{_libdir}/grass%{grassfix}/lib
EOF

%files
%doc AUTHORS COPYING INSTALL README CHANGES
%attr(0755,root,root) %{_bindir}/*
%{_sysconfdir}/ld.so.conf.d/*
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/*/*/*/*
%{_libdir}/grass%{grassfix}/grass%{grassfix}.tmp
%{_libdir}/grass%{grassfix}/bin
%{_libdir}/grass%{grassfix}/bwidget
%{_libdir}/grass%{grassfix}/demolocation
%{_libdir}/grass%{grassfix}/docs
%{_libdir}/grass%{grassfix}/driver
%{_libdir}/grass%{grassfix}/etc
%{_libdir}/grass%{grassfix}/fonts
%{_libdir}/grass%{grassfix}/include
%{_libdir}/grass%{grassfix}/lib
%{_libdir}/grass%{grassfix}/locale
%{_libdir}/grass%{grassfix}/man
%{_libdir}/grass%{grassfix}/scripts
%{_libdir}/grass%{grassfix}/tools
%attr(1777,root,root) %{_libdir}/grass%{grassfix}/locks


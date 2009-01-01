%define grassfix 63

Name: 		grass
Version: 	6.2.3
Release: 	%mkrel 6
Group: 		Sciences/Geosciences
Summary: 	Geographic Resources Analysis Support System
License: 	GPLv2+
URL: 		http://grass.itc.it/
Source:		http://grass.itc.it/grass%{grassfix}/source/grass-%{version}.tar.gz
Source2: 	grass5_48.png.bz2
Source3: 	grass5_32.png.bz2
Source4: 	grass5_16.png.bz2
Patch0:		grass-6.2.3-fix-str-fmt.patch
Patch1:		grass-6.2.3-fix-linkage.patch
BuildRoot: 	%{_tmppath}/%{name}-%{version}-root
Requires: xterm 
Requires: tk 
Requires: tcl
BuildRequires:  libxmu-devel
BuildRequires: 	png-devel 
BuildRequires:  jpeg-devel 
BuildRequires:  tiff-devel 
BuildRequires:  gd-devel >= 2.0 
BuildRequires:  freetype2-devel
BuildRequires: 	MesaGLU-devel 
BuildRequires:  unixODBC-devel 
BuildRequires:  fftw-devel 
BuildRequires:  lesstif-devel
BuildRequires: 	tk tk-devel
BuildRequires:  ncurses-devel 
BuildRequires:  zlib-devel 
BuildRequires:  gdbm-devel 
BuildRequires:  readline-devel 
BuildRequires:  postgresql-devel
BuildRequires:	gcc-gfortran 
BuildRequires:  gdal-devel >= 1.2.0 
BuildRequires:  flex 
BuildRequires:  bison
BuildRequires:  proj-devel proj >= 4.4.7
BuildRequires:  tcl tcl-devel
BuildRequires:  fftw-devel
BuildRequires:	cfitsio-devel
BuildRequires:	unixODBC-devel
BuildRequires:  mysql-devel
BuildRequires:	termcap-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	freetype-devel
BuildRequires:	python-devel
BuildRequires:	sqlite-devel
BuildRequires:	lzma
# deal with Xorg split
BuildRequires:	mesaglw-devel

Obsoletes:	grass57
Provides:	grass57 = %{version}-%{release}

%description
GRASS (Geographic Resources Analysis Support System) is an 
open source, Free Software Geographical Information System (GIS)
with raster, topological vector, image processing, and graphics
production functionality that operates on various platforms 
through a graphical user interface and shell in X-Window.

%prep
%setup -q
%patch0 -p1 -b .str
%patch1 -p0 -b .linkage

%build
%configure \
	--with-dbm-includes=%{_includedir}/gdbm/ \
%if %mdkversion >= 200900
	--with-postgres-includes=%{_includedir}/ \
%else
	--with-postgres-includes='%{_includedir}/pgsql %{_includedir}/pgsql/internal' \
%endif
	--with-freetype \
	--with-freetype-includes=%{_includedir}/freetype2 \
	--with-motif \
	--with-opengl-libs=%{_libdir} \
	--with-motif-libs=%{_libdir} \
	--with-motif-libs=%{_libdir} \
	--with-motif-includes=%{_includedir} \
	--with-gdal  \
	--with-mysql --with-mysql-includes=%{_includedir}/mysql \
	--with-odbc \
	--enable-largefile \
%if %mdkversion >= 200900
	--with-ffmpeg --with-ffmpeg-includes=%{_includedir}/libav* \
%else
	--with-ffmpeg --with-ffmpeg-includes=%{_includedir}/ffmpeg \
%endif
	--with-curses \
	--with-python \
	--with-sqlite \
	--with-cxx \
	--with-proj-share=%{_datadir}/proj \
	--with-nls \
	--with-readline \
	%{?_with_cvs:--with-grass50=`pwd`/../grass50_%{cvsver}}

#Options that aren't really used
#	--with-blas \
#	--with-lapack \
#	--with-dbm \

#Fix messy grass readline misdetection:
perl -pi -e "s/^READLINELIB .*\$/READLINELIB         =  -lreadline -ltermcap/g" include/Make/Platform.make
perl -pi -e "s/^HISTORYLIB.*\$/HISTORYLIB          =  -lhistory/g" include/Make/Platform.make
perl -pi -e 's,/\* #undef HAVE_READLINE_READLINE_H \*/,#define HAVE_READLINE_READLINE_H 1,g' include/config.h
%if %{?_with_cvs:1}%{!?_with_cvs:0}
make mix
%endif
#r.mapcalc not building first time around:
make||make

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf "$RPM_BUILD_ROOT"
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
mkdir -p $RPM_BUILD_ROOT/%{_menudir}
#%makeinstall_std INST_DIR=%{_libdir}/grass%{grassfix}
# Actions in make install that don't take into account packaging in a place different to running:
sed -e 's|^GISBASE.*|GISBASE=%{_libdir}/grass%{grassfix}|' \
 bin.%{_target_platform}/grass%{grassfix} > $RPM_BUILD_ROOT/%{_bindir}/grass%{grassfix}
chmod a+x $RPM_BUILD_ROOT/usr/bin/grass%{grassfix}

mkdir -p %{buildroot}/%{_libdir}/grass%{grassfix}
cp -a dist.%{_target_platform}/* %{buildroot}/%{_libdir}/grass%{grassfix}

# Add makefiles to includes:
cp -a include/Make %{buildroot}/%{_libdir}/grass%{grassfix}/include/

# Manually archive the man pages:
lzma $RPM_BUILD_ROOT/%{_libdir}/grass%{grassfix}/man/man?/*

mkdir $RPM_BUILD_ROOT/%{_libdir}/grass%{grassfix}/locks/

mkdir -p $RPM_BUILD_ROOT%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps

bzcat %{SOURCE2} > $RPM_BUILD_ROOT%{_iconsdir}/hicolor/48x48/apps/%{name}.png
bzcat %{SOURCE3} > $RPM_BUILD_ROOT%{_iconsdir}/hicolor/32x32/apps/%{name}.png
bzcat %{SOURCE4} > $RPM_BUILD_ROOT%{_iconsdir}/hicolor/16x16/apps/%{name}.png

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Grass%{grassfix}
Comment=Geographic Resources Analysis Support System
Exec=%{_bindir}/grass%{grassfix} 
Icon=%{name}
Terminal=true
Type=Application
Categories=Science;Geology;
EOF

mkdir -p $RPM_BUILD_ROOT%_sysconfdir/ld.so.conf.d
cat > $RPM_BUILD_ROOT%_sysconfdir/ld.so.conf.d/grass.conf << EOF
%_libdir/grass62/lib
EOF

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf "$RPM_BUILD_ROOT"

%post
%if %mdkversion < 200900
%update_menus
%update_icon_cache hicolor
%endif
%if %mdkversion < 200900
/sbin/ldconfig
%endif

%postun
%if %mdkversion < 200900
%clean_menus
%clean_icon_cache hicolor
%endif
%if %mdkversion < 200900
/sbin/ldconfig
%endif

%files
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/*
%_sysconfdir/ld.so.conf.d/*
%{_libdir}/grass%{grassfix}/
%{_datadir}/applications/mandriva-grass.desktop
%{_iconsdir}/*/*/*/*
%attr(1777,root,root) %{_libdir}/grass%{grassfix}/locks
%doc AUTHORS COPYING INSTALL README CHANGES

%define cvs_y 2004
%define cvs_m 05
%define cvs_d 05
%define cvsver exp_%{cvs_y}_%{cvs_m}_%{cvs_d}
%define version	6.2.2
%define rel 1
%define release %mkrel %rel
#define release %{?_with_cvs:%mkrel -c %{cvs_y}%{cvs_m}%{cvs_d} %rel}%{!?_with_cvs:%mkrel %rel}
%define grassfix 62
#if %mdkversion >= 200710
%define name grass
#Obsoletes: grass%{grassfix}
#else
#define name grass%{?grassfix:%grassfix}
#endif

%{?_with_cvs: %define build_cvs 1}

Summary: 	Geographic Resources Analysis Support System
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
Group: 		Sciences/Geosciences
License: 	GPL
URL: 		http://grass.itc.it/
%if %{?_with_cvs:1}%{!?_with_cvs:0}
Source: 	http://grass.itc.it/%{name}/source/snapshot/%{name}src_cvs_snapshot_%{cvsver}.tar.gz
Source1: 	http://grass.itc.it/grass50/source/snapshot/grass50src_cvs_snapshot_%{cvsver}.tar.gz
%else
Source:		http://grass.itc.it/grass%{grassfix}/source/grass-%{version}.tar.gz
%endif
Source2: 	grass5_48.png.bz2
Source3: 	grass5_32.png.bz2
Source4: 	grass5_16.png.bz2
Patch2:		grass51-20030614-blas-lapack-libs.patch
BuildRoot: 	%{_tmppath}/%{name}-%{version}-root

Requires:	xterm 
Requires:       tk 
Requires:       tcl

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
BuildRequires:  libblas-devel 
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
%if %mdkversion >= 200700
# deal with Xorg split
BuildRequires:	mesaglw-devel
%endif

Obsoletes:	grass57
Provides:	grass57 = %{version}-%{release}

%description
GRASS (Geographic Resources Analysis Support System) is an 
open source, Free Software Geographical Information System (GIS)
with raster, topological vector, image processing, and graphics
production functionality that operates on various platforms 
through a graphical user interface and shell in X-Window.

%prep
%setup -q %{?_with_cvs:-b1 -n %{name}_%{cvsver}}%{!?_with_cvs:-n grass-%{version}}
#patch2
autoconf

%build
export LDFLAGS="-L/usr/X11R6/%{_lib}"
%configure \
	--with-dbm-includes=%{_includedir}/gdbm/ \
	--with-postgres-includes='%{_includedir}/pgsql %{_includedir}/pgsql/internal' \
	--with-freetype \
	--with-freetype-includes=%{_includedir}/freetype2 \
	--with-motif \
%if %mdkversion >= 200700
	--with-opengl-libs=%{_libdir} \
	--with-motif-libs=%{_libdir} \
	--with-motif-libs=%{_libdir} \
	--with-motif-includes=%{_includedir} \
%else
	--with-opengl-libs=%{_prefix}/X11R6/%{_lib} \
	--with-motif-includes=%{_prefix}/X11R6/include \
%endif
	--with-gdal  \
	--with-mysql --with-mysql-includes=%{_includedir}/mysql \
	--with-odbc \
	--enable-largefile \
	--with-ffmpeg --with-ffmpeg-includes=%{_includedir}/ffmpeg \
	--with-curses \
	--with-python \
	--with-sqlite \
	--with-cxx \
	--with-nls \
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
#cp $RPM_BUILD_PATH/bin.i586-mandrake-linux-gnu/gmake5 $RPM_BUILD_ROOT/usr/bin
#cp $RPM_BUILD_PATH/bin.i586-mandrake-linux-gnu/gmakelinks5 $RPM_BUILD_ROOT/usr/bin

mkdir -p %{buildroot}/%{_libdir}/grass%{grassfix}
cp -a dist.%{_target_platform}/* %{buildroot}/%{_libdir}/grass%{grassfix}

# Add makefiles to includes:
cp -a include/Make %{buildroot}/%{_libdir}/grass%{grassfix}/include/

# Manually bzip2 the man pages:
bzip2 $RPM_BUILD_ROOT/%{_libdir}/grass%{grassfix}/man/man?/*

mkdir $RPM_BUILD_ROOT/%{_libdir}/grass%{grassfix}/locks/

mkdir -p $RPM_BUILD_ROOT%{_liconsdir} $RPM_BUILD_ROOT%{_iconsdir} $RPM_BUILD_ROOT%{_miconsdir}

bzcat %{SOURCE2} > $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png
bzcat %{SOURCE3} > $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
bzcat %{SOURCE4} > $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Grass%{grassfix}
Comment=Geographic Resources Analysis Support System
Exec=%{_bindir}/grass%{grassfix} 
Icon=%{name}
Terminal=true
Type=Application
Categories=X-MandrivaLinux-MoreApplications-Sciences-Geosciences;Science;Geology;
EOF

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf "$RPM_BUILD_ROOT"

%post
%update_menus

%postun
%clean_menus

%files
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/*
%{_libdir}/grass%{grassfix}/
%{_datadir}/applications/mandriva-grass.desktop
%{_miconsdir}/*.png
%{_liconsdir}/*.png
%{_iconsdir}/*.png
%attr(1777,root,root) %{_libdir}/grass%{grassfix}/locks
%doc AUTHORS COPYING INSTALL README CHANGES

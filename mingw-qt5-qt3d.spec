%?mingw_package_header

# Override the __debug_install_post argument as this package
# contains both native as well as cross compiled binaries
%global __debug_install_post %%{mingw_debug_install_post}; %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%%{?buildsubdir}" %{nil}

%global qt_module qt3d
#%%global pre beta1

#%%global snapshot_date 20140525
#%%global snapshot_rev bdb98ba

%if 0%{?snapshot_date}
%global source_folder qt-%{qt_module}
%else
%global source_folder %{qt_module}-opensource-src-%{version}%{?pre:-%{pre}}
%endif

# first two digits of version
%global release_version %(echo %{version} | awk -F. '{print $1"."$2}')

Name:           mingw-qt5-%{qt_module}
Version:        5.6.0
Release:        4%{?pre:.%{pre}}%{?snapshot_date:.git%{snapshot_date}.%{snapshot_rev}}%{?dist}
Summary:        Qt5 for Windows - Qt3d component

License:        GPLv3 with exceptions or LGPLv2 with exceptions
Group:          Development/Libraries
URL:            http://qt.io/

%if 0%{?snapshot_date}
# To regenerate:
# wget http://qt.gitorious.org/qt/%{qt_module}/archive-tarball/%{snapshot_rev} -O qt5-%{qt_module}-%{snapshot_rev}.tar.gz
Source0:        qt5-%{qt_module}-%{snapshot_rev}.tar.gz
%else
%if "%{?pre}" != ""
Source0:        http://download.qt-project.org/development_releases/qt/%{release_version}/%{version}-%{pre}/submodules/%{qt_module}-opensource-src-%{version}-%{pre}.tar.xz
%else
Source0:        http://download.qt-project.org/official_releases/qt/%{release_version}/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz
%endif
%endif

BuildRequires:  mingw32-filesystem >= 96
BuildRequires:  mingw32-qt5-qtbase >= 5.6.0
BuildRequires:  mingw32-qt5-qtbase-devel >= 5.6.0
BuildRequires:  mingw32-qt5-qtdeclarative >= 5.6.0

BuildRequires:  mingw64-filesystem >= 96
BuildRequires:  mingw64-qt5-qtbase >= 5.6.0
BuildRequires:  mingw64-qt5-qtbase-devel >= 5.6.0
BuildRequires:  mingw64-qt5-qtdeclarative >= 5.6.0

# This package depends on QtOpenGLExtensions which is only available as a static library
# See http://code.qt.io/cgit/qt/qtbase.git/commit/?id=a2ddf3dfe066bb4e58de1d11b1800efcd05fb3a0
BuildRequires:  mingw32-qt5-qtbase-static
BuildRequires:  mingw64-qt5-qtbase-static

BuildRequires:  zlib-devel

# Make sure -lz is added to the LDFLAGS
Patch0:         qt3d-fix-zlib-linker-flags.patch


%description
This package contains the Qt software toolkit for developing
cross-platform applications.

This is the Windows version of Qt, for use in conjunction with the
Fedora Windows cross-compiler.


# Win32
%package -n mingw32-qt5-%{qt_module}
Summary:        Qt5 for Windows - Qt3d component
BuildArch:      noarch

%description -n mingw32-qt5-%{qt_module}
This package contains the Qt software toolkit for developing
cross-platform applications.

This is the Windows version of Qt, for use in conjunction with the
Fedora Windows cross-compiler.

%package -n mingw32-qt5-%{qt_module}-tools
Summary:        Qt5 for Windows - Native tools for the Qt3d component
Requires:       mingw32-qt5-%{qt_module} = %{version}-%{release}

%description -n mingw32-qt5-%{qt_module}-tools
This package contains the Qt software toolkit for developing
cross-platform applications.

This is the Windows version of Qt, for use in conjunction with the
Fedora Windows cross-compiler.


# Win64
%package -n mingw64-qt5-%{qt_module}
Summary:        Qt5 for Windows - Qt3d component
BuildArch:      noarch

%description -n mingw64-qt5-%{qt_module}
This package contains the Qt software toolkit for developing
cross-platform applications.

This is the Windows version of Qt, for use in conjunction with the
Fedora Windows cross-compiler.

%package -n mingw64-qt5-%{qt_module}-tools
Summary:        Qt5 for Windows - Native tools for the Qt3d component
Requires:       mingw64-qt5-%{qt_module} = %{version}-%{release}

%description -n mingw64-qt5-%{qt_module}-tools
This package contains the Qt software toolkit for developing
cross-platform applications.

This is the Windows version of Qt, for use in conjunction with the
Fedora Windows cross-compiler.


%?mingw_debug_package


%prep
%setup -q -n %{source_folder}
%patch0 -p1

%if 0%{?snapshot_date}
# Make sure the syncqt tool is run because we're using a git snapshot
# Otherwise the build fails against Qt 5.1
mkdir .git
%endif


%build
%mingw_qmake_qt5 ../%{qt_module}.pro
%mingw_make %{?_smp_mflags}


%install
%mingw_make install INSTALL_ROOT=$RPM_BUILD_ROOT

# .prl files aren't interesting for us
find $RPM_BUILD_ROOT -name "*.prl" -delete


# Win32
%files -n mingw32-qt5-%{qt_module}
%doc LICENSE.GPL LICENSE.LGPLv3
%{mingw32_bindir}/Qt53DCore.dll
%{mingw32_bindir}/Qt53DInput.dll
%{mingw32_bindir}/Qt53DLogic.dll
%{mingw32_bindir}/Qt53DQuick.dll
%{mingw32_bindir}/Qt53DQuickInput.dll
%{mingw32_bindir}/Qt53DQuickRender.dll
%{mingw32_bindir}/Qt53DRender.dll
%{mingw32_includedir}/qt5/Qt3DCore/
%{mingw32_includedir}/qt5/Qt3DInput/
%{mingw32_includedir}/qt5/Qt3DLogic/
%{mingw32_includedir}/qt5/Qt3DQuick/
%{mingw32_includedir}/qt5/Qt3DQuickInput/
%{mingw32_includedir}/qt5/Qt3DQuickRender/
%{mingw32_includedir}/qt5/Qt3DRender/
%{mingw32_libdir}/libQt53DCore.dll.a
%{mingw32_libdir}/libQt53DInput.dll.a
%{mingw32_libdir}/libQt53DLogic.dll.a
%{mingw32_libdir}/libQt53DQuick.dll.a
%{mingw32_libdir}/libQt53DQuickInput.dll.a
%{mingw32_libdir}/libQt53DQuickRender.dll.a
%{mingw32_libdir}/libQt53DRender.dll.a
%dir %{mingw32_libdir}/qt5/plugins/sceneparsers/
%{mingw32_libdir}/qt5/plugins/sceneparsers/gltfsceneparser.dll
%{mingw32_libdir}/cmake/Qt53DCore/
%{mingw32_libdir}/cmake/Qt53DInput/
%{mingw32_libdir}/cmake/Qt53DLogic/
%{mingw32_libdir}/cmake/Qt53DQuick/
%{mingw32_libdir}/cmake/Qt53DQuickInput/
%{mingw32_libdir}/cmake/Qt53DQuickRender/
%{mingw32_libdir}/cmake/Qt53DRender/
%{mingw32_libdir}/pkgconfig/Qt53DCore.pc
%{mingw32_libdir}/pkgconfig/Qt53DInput.pc
%{mingw32_libdir}/pkgconfig/Qt53DLogic.pc
%{mingw32_libdir}/pkgconfig/Qt53DQuick.pc
%{mingw32_libdir}/pkgconfig/Qt53DQuickInput.pc
%{mingw32_libdir}/pkgconfig/Qt53DQuickRender.pc
%{mingw32_libdir}/pkgconfig/Qt53DRender.pc
%{mingw32_datadir}/qt5/mkspecs/modules/qt_lib_3dcore.pri
%{mingw32_datadir}/qt5/mkspecs/modules/qt_lib_3dcore_private.pri
%{mingw32_datadir}/qt5/mkspecs/modules/qt_lib_3dinput.pri
%{mingw32_datadir}/qt5/mkspecs/modules/qt_lib_3dinput_private.pri
%{mingw32_datadir}/qt5/mkspecs/modules/qt_lib_3dlogic.pri
%{mingw32_datadir}/qt5/mkspecs/modules/qt_lib_3dlogic_private.pri
%{mingw32_datadir}/qt5/mkspecs/modules/qt_lib_3dquick.pri
%{mingw32_datadir}/qt5/mkspecs/modules/qt_lib_3dquick_private.pri
%{mingw32_datadir}/qt5/mkspecs/modules/qt_lib_3dquickinput.pri
%{mingw32_datadir}/qt5/mkspecs/modules/qt_lib_3dquickinput_private.pri
%{mingw32_datadir}/qt5/mkspecs/modules/qt_lib_3dquickrender.pri
%{mingw32_datadir}/qt5/mkspecs/modules/qt_lib_3dquickrender_private.pri
%{mingw32_datadir}/qt5/mkspecs/modules/qt_lib_3drender.pri
%{mingw32_datadir}/qt5/mkspecs/modules/qt_lib_3drender_private.pri
%dir %{mingw32_datadir}/qt5/qml/Qt3D/
%dir %{mingw32_datadir}/qt5/qml/Qt3D/Core/
%{mingw32_datadir}/qt5/qml/Qt3D/Core/qmldir
%{mingw32_datadir}/qt5/qml/Qt3D/Core/quick3dcoreplugin.dll
%dir %{mingw32_datadir}/qt5/qml/Qt3D/Input/
%{mingw32_datadir}/qt5/qml/Qt3D/Input/qmldir
%{mingw32_datadir}/qt5/qml/Qt3D/Input/quick3dinputplugin.dll
%dir %{mingw32_datadir}/qt5/qml/Qt3D/Logic
%{mingw32_datadir}/qt5/qml/Qt3D/Logic/qmldir
%{mingw32_datadir}/qt5/qml/Qt3D/Logic/quick3dlogicplugin.dll
%dir %{mingw32_datadir}/qt5/qml/Qt3D/Render/
%{mingw32_datadir}/qt5/qml/Qt3D/Render/qmldir
%{mingw32_datadir}/qt5/qml/Qt3D/Render/quick3drenderplugin.dll
%dir %{mingw32_datadir}/qt5/qml/QtQuick/Scene3D/
%{mingw32_datadir}/qt5/qml/QtQuick/Scene3D/qmldir
%{mingw32_datadir}/qt5/qml/QtQuick/Scene3D/qtquickscene3dplugin.dll

%files -n mingw32-qt5-%{qt_module}-tools
%{_prefix}/%{mingw32_target}/bin/qt5/qgltf


# Win64
%files -n mingw64-qt5-%{qt_module}
%doc LICENSE.GPL LICENSE.LGPLv3
%{mingw64_bindir}/Qt53DCore.dll
%{mingw64_bindir}/Qt53DInput.dll
%{mingw64_bindir}/Qt53DLogic.dll
%{mingw64_bindir}/Qt53DQuick.dll
%{mingw64_bindir}/Qt53DQuickInput.dll
%{mingw64_bindir}/Qt53DQuickRender.dll
%{mingw64_bindir}/Qt53DRender.dll
%{mingw64_includedir}/qt5/Qt3DCore/
%{mingw64_includedir}/qt5/Qt3DInput/
%{mingw64_includedir}/qt5/Qt3DLogic/
%{mingw64_includedir}/qt5/Qt3DQuick/
%{mingw64_includedir}/qt5/Qt3DQuickInput/
%{mingw64_includedir}/qt5/Qt3DQuickRender/
%{mingw64_includedir}/qt5/Qt3DRender/
%{mingw64_libdir}/libQt53DCore.dll.a
%{mingw64_libdir}/libQt53DInput.dll.a
%{mingw64_libdir}/libQt53DLogic.dll.a
%{mingw64_libdir}/libQt53DQuick.dll.a
%{mingw64_libdir}/libQt53DQuickInput.dll.a
%{mingw64_libdir}/libQt53DQuickRender.dll.a
%{mingw64_libdir}/libQt53DRender.dll.a
%dir %{mingw64_libdir}/qt5/plugins/sceneparsers/
%{mingw64_libdir}/qt5/plugins/sceneparsers/gltfsceneparser.dll
%{mingw64_libdir}/cmake/Qt53DCore/
%{mingw64_libdir}/cmake/Qt53DInput/
%{mingw64_libdir}/cmake/Qt53DLogic/
%{mingw64_libdir}/cmake/Qt53DQuickInput/
%{mingw64_libdir}/cmake/Qt53DQuick/
%{mingw64_libdir}/cmake/Qt53DQuickRender/
%{mingw64_libdir}/cmake/Qt53DRender/
%{mingw64_libdir}/pkgconfig/Qt53DCore.pc
%{mingw64_libdir}/pkgconfig/Qt53DInput.pc
%{mingw64_libdir}/pkgconfig/Qt53DLogic.pc
%{mingw64_libdir}/pkgconfig/Qt53DQuick.pc
%{mingw64_libdir}/pkgconfig/Qt53DQuickInput.pc
%{mingw64_libdir}/pkgconfig/Qt53DQuickRender.pc
%{mingw64_libdir}/pkgconfig/Qt53DRender.pc
%{mingw64_datadir}/qt5/mkspecs/modules/qt_lib_3dcore.pri
%{mingw64_datadir}/qt5/mkspecs/modules/qt_lib_3dcore_private.pri
%{mingw64_datadir}/qt5/mkspecs/modules/qt_lib_3dinput.pri
%{mingw64_datadir}/qt5/mkspecs/modules/qt_lib_3dinput_private.pri
%{mingw64_datadir}/qt5/mkspecs/modules/qt_lib_3dlogic.pri
%{mingw64_datadir}/qt5/mkspecs/modules/qt_lib_3dlogic_private.pri
%{mingw64_datadir}/qt5/mkspecs/modules/qt_lib_3dquick.pri
%{mingw64_datadir}/qt5/mkspecs/modules/qt_lib_3dquick_private.pri
%{mingw64_datadir}/qt5/mkspecs/modules/qt_lib_3dquickinput.pri
%{mingw64_datadir}/qt5/mkspecs/modules/qt_lib_3dquickinput_private.pri
%{mingw64_datadir}/qt5/mkspecs/modules/qt_lib_3dquickrender.pri
%{mingw64_datadir}/qt5/mkspecs/modules/qt_lib_3dquickrender_private.pri
%{mingw64_datadir}/qt5/mkspecs/modules/qt_lib_3drender.pri
%{mingw64_datadir}/qt5/mkspecs/modules/qt_lib_3drender_private.pri
%dir %{mingw64_datadir}/qt5/qml/Qt3D/
%dir %{mingw64_datadir}/qt5/qml/Qt3D/Core/
%{mingw64_datadir}/qt5/qml/Qt3D/Core/qmldir
%{mingw64_datadir}/qt5/qml/Qt3D/Core/quick3dcoreplugin.dll
%dir %{mingw64_datadir}/qt5/qml/Qt3D/Input/
%{mingw64_datadir}/qt5/qml/Qt3D/Input/qmldir
%{mingw64_datadir}/qt5/qml/Qt3D/Input/quick3dinputplugin.dll
%dir %{mingw64_datadir}/qt5/qml/Qt3D/Logic
%{mingw64_datadir}/qt5/qml/Qt3D/Logic/qmldir
%{mingw64_datadir}/qt5/qml/Qt3D/Logic/quick3dlogicplugin.dll
%dir %{mingw64_datadir}/qt5/qml/Qt3D/Render/
%{mingw64_datadir}/qt5/qml/Qt3D/Render/qmldir
%{mingw64_datadir}/qt5/qml/Qt3D/Render/quick3drenderplugin.dll
%dir %{mingw64_datadir}/qt5/qml/QtQuick/Scene3D/
%{mingw64_datadir}/qt5/qml/QtQuick/Scene3D/qmldir
%{mingw64_datadir}/qt5/qml/QtQuick/Scene3D/qtquickscene3dplugin.dll

%files -n mingw64-qt5-%{qt_module}-tools
%{_prefix}/%{mingw64_target}/bin/qt5/qgltf


%changelog
* Fri Feb 03 2017 Jajauma's Packages <jajauma@yandex.ru> - 5.6.0-4
- Rebuild with GCC 5.4.0

* Wed Feb 01 2017 Jajauma's Packages <jajauma@yandex.ru> - 5.6.0-3
- Don't require qtquick1 for building

* Sat May  7 2016 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.6.0-2
- Add BR: mingw{32,64}-qt5-qtbase-devel

* Sun Apr 10 2016 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.6.0-1
- Update to 5.6.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Aug  7 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.5.0-1
- Update to 5.5.0
- Added BR: mingw{32,64}-qt5-qtbase-static as this package depends
  on QtOpenGLExtensions which is only available as a static library

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.0-0.13.git20140525.bdb98ba
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.0-0.12.git20140525.bdb98ba
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May 25 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.11.git20140525.bdb98ba
- Update to 20140525 snapshot (rev bdb98ba)

* Sun Jan 12 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.10.git20130923.7433868
- Don't carry .dll.debug files in main package

* Wed Jan  8 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.9.git20130923.7433868
- Dropped manual rename of import libraries

* Sun Jan  5 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.8.git20130923.7433868
- Update to 20130923 snapshot (rev 7433868)
  This is the last Qt 5.2 based revision

* Sun Dec 01 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.7.git20130510.0158ce78
- Fix FTBFS against Qt 5.2

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.0-0.6.git20130510.0158ce78
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.5.git20130510.0158ce78
- Make sure the syncqt tool is run because we're using a git snapshot

* Fri May 10 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.4.git20130510.0158ce78
- Update to 20130510 snapshot (rev 0158ce78)

* Sat Jan 12 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.3.git20121111.e4d3ccac
- Fix filelist

* Sun Nov 11 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.2.beta1.git20121111.e4d3ccac
- Update to 20121111 snapshot (rev e4d3ccac)
- Rebuild against latest mingw-qt5-qtbase
- Dropped pkg-config rename hack as it's unneeded now

* Wed Sep 12 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.1.beta1
- Initial release


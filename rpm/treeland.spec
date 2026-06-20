Name:           treeland
Version:        0.8.5
Release:        1%{?dist}
Summary:        Treeland - Wayland Compositor for Lingmo OS
License:        GPL-3.0-or-later
URL:            https://github.com/LingmoOS/treeland
Source0:        treeland-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  cmake >= 3.25
BuildRequires:  extra-cmake-modules
BuildRequires:  pkgconfig(Qt6Core)
BuildRequires:  pkgconfig(Qt6Gui)
BuildRequires:  pkgconfig(Qt6Quick)
BuildRequires:  pkgconfig(Qt6WaylandClient)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libinput)

%description
Treeland is a Wayland compositor for the Lingmo desktop environment,
built on modern graphics stack with Qt6 and Wayland protocols.

%prep
%autosetup -n %{name}-%{version}

%build
%cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_TESTING=OFF \
    -DWITH_SUBMODULE_WAYLIB=ON
%cmake_build

%install
%cmake_install

%files
%doc README.md
%license LICENSE*
%{_bindir}/treeland
%{_libexecdir}/treeland/
%{_datadir}/treeland/
%{_datadir}/dbus-1/services/*.service
%{_datadir}/wayland-sessions/treeland.desktop
%{_libdir}/treeland/

%changelog
* Tue Jun 18 2025 LingmoOS Build System <dev@lingmo.os> - %{version}-1
- Initial RPM packaging for local source build

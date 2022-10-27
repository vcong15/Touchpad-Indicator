Name: touchpad-indicator
# Refer to debian/changelog for version information
Version: 2.2.3
Release: alt1

Summary: An indicator for the touchpad

License: GPLv3
Group: System/Configuration/Hardware
Url: https://github.com/atareao/Touchpad-Indicator

Source: %name-%version.tar

BuildArch: noarch

BuildRequires: rpm-build-python3
Requires: python3-module-pyudev
Requires: python3-module-evdev
Requires: python3-module-xlib
Requires: laptop-mode-tools

%description
With Touchpad Indicator you can enable or disable the touchpad, 
with shortcuts or by clicking on menu.
Besides, it enables or disables the touchpad, 
when the computer returns from hibernation.

%prep
%setup
# Fix locales' directory address in sources
find . -type f -exec \
    sed -i -e 's:locale-langpack:locale:g' '{}' \;
  
%build

%install
# Process debian/install file (dh_install job of debhelper)
while read filename dirname ; do
    mkdir -p %buildroot/$dirname/
    install -m644 $filename %buildroot/$dirname/
done < debian/install
chmod 755 %buildroot/usr/bin/%name
chmod 755 %buildroot/etc/pm/sleep.d/00_check_touchpad_status
chmod 755 %buildroot/usr/lib/systemd/system-sleep/00_check_touchpad_status_systemd
chmod 755 %buildroot/usr/share/%name/*.py
# Process locale handling in debian/rules, being aware of comment mistype 'comile'->'compile'
awk '/# Create languages directories/{f=1; next}/# End (comile|compile) languages/\
{f=0}{sub(/\${CURDIR}\/debian\/touchpad-indicator\//, "%buildroot/")}f' \
debian/rules | bash

%find_lang %name
%files -f %name.lang
%_sysconfdir/pm/sleep.d/00_check_touchpad_status
%_bindir/touchpad-indicator
%prefix/lib/systemd/system-sleep/00_check_touchpad_status_systemd
%_datadir/applications/touchpad-indicator.desktop
%_datadir/glib-2.0/schemas/*.gschema.xml
%_datadir/touchpad-indicator
%_iconsdir/hicolor/*/apps/*

%changelog
* Thu Oct 27 2022 Alexey Ivakhnenko <vcong@altlinux.org> 2.2.3-alt1
- Initial build for Sisyphus

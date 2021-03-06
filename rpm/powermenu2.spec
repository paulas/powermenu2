Name:       powermenu2

%{!?qtc_qmake:%define qtc_qmake %qmake}
%{!?qtc_qmake5:%define qtc_qmake5 %qmake5}
%{!?qtc_make:%define qtc_make make}
%{?qtc_builddir:%define _builddir %qtc_builddir}
Summary:    PowerMenu 2
Version:    1.3.0
Release:    1
Group:      Qt/Qt
License:    WTFPL
URL:        https://openrepos.net/content/coderus/powermenu2
Source0:    %{name}-%{version}.tar.bz2
Requires:   sailfishsilica-qt5 >= 0.10.9
Requires:   sailfish-version >= 2.0.2
Conflicts:  powermenu
BuildRequires:  pkgconfig(sailfishapp) >= 1.0.2
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Qml)
BuildRequires:  pkgconfig(Qt5Quick)
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig(mlite5)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(dbus-glib-1)

Summary: fancy menu and configuration for power key actions

%description
Powermenu - fancy menu and configuration for power key actions


%package -n sailfishos-ambience-powermenu2
Summary:    Ambience Powermenu2
Group:      Qt/Qt
License:    WTFPL
Requires:   patchmanager
Requires:   sailfish-version >= 2.0.2
Requires:   %{name} >= %{version}
BuildArch:  noarch

%description -n sailfishos-ambience-powermenu2
Patch replacing ambience switcher top content by Powermenu2

%prep
%setup -q -n %{name}-%{version}

%build

%qtc_qmake5  \
    VERSION=%{version}

%qtc_make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%qmake5_install

mkdir -p %{buildroot}/usr/lib/systemd/user/post-user-session.target.wants
ln -s ../powermenu.service %{buildroot}/usr/lib/systemd/user/post-user-session.target.wants/powermenu.service

%pre
systemctl-user stop powermenu.service

if /sbin/pidof powermenu2-daemon > /dev/null; then
killall powermenu2-daemon || true
fi

if /sbin/pidof powermenu2-gui > /dev/null; then
killall powermenu2-gui || true
fi

if /sbin/pidof powermenu2-flashlight > /dev/null; then
killall powermenu2-flashlight || true
fi

%preun
systemctl-user stop powermenu.service

if [ $1 -eq 0 ] ; then
DSBA=$DBUS_SESSION_BUS_ADDRESS
export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/100000/dbus/user_bus_socket
dbus-send --system --type=method_call --dest=com.nokia.mce /com/nokia/mce/request com.nokia.mce.request.set_config "string:/system/osso/dsm/powerkey/long_press_delay" "variant:int32:1500" || :
dbus-send --system --type=method_call --dest=com.nokia.mce /com/nokia/mce/request com.nokia.mce.request.set_config "string:/system/osso/dsm/powerkey/double_press_delay" "variant:int32:400" || :
dbus-send --system --type=method_call --dest=com.nokia.mce /com/nokia/mce/request com.nokia.mce.request.set_config "string:/system/osso/dsm/powerkey/actions_single_on" "variant:string:blank,tklock" || :
dbus-send --system --type=method_call --dest=com.nokia.mce /com/nokia/mce/request com.nokia.mce.request.set_config "string:/system/osso/dsm/powerkey/actions_double_on" "variant:string:blank,tklock,devlock" || :
dbus-send --system --type=method_call --dest=com.nokia.mce /com/nokia/mce/request com.nokia.mce.request.set_config "string:/system/osso/dsm/powerkey/actions_long_on" "variant:string:dbus1" || :
dbus-send --system --type=method_call --dest=com.nokia.mce /com/nokia/mce/request com.nokia.mce.request.set_config "string:/system/osso/dsm/powerkey/actions_single_off" "variant:string:unblank" || :
dbus-send --system --type=method_call --dest=com.nokia.mce /com/nokia/mce/request com.nokia.mce.request.set_config "string:/system/osso/dsm/powerkey/actions_double_off" "variant:string:unblank,tkunlock,dbus2" || :
dbus-send --system --type=method_call --dest=com.nokia.mce /com/nokia/mce/request com.nokia.mce.request.set_config "string:/system/osso/dsm/powerkey/actions_long_off" "variant:string:" || :
dbus-send --system --type=method_call --dest=com.nokia.mce /com/nokia/mce/request com.nokia.mce.request.set_config "string:/system/osso/dsm/powerkey/dbus_action1" "variant:string:power-key-menu" || :
dbus-send --system --type=method_call --dest=com.nokia.mce /com/nokia/mce/request com.nokia.mce.request.set_config "string:/system/osso/dsm/powerkey/dbus_action2" "variant:string:double-power-key" || :
dbus-send --system --type=method_call --dest=com.nokia.mce /com/nokia/mce/request com.nokia.mce.request.set_config "string:/system/osso/dsm/powerkey/dbus_action3" "variant:string:event3" || :
dbus-send --system --type=method_call --dest=com.nokia.mce /com/nokia/mce/request com.nokia.mce.request.set_config "string:/system/osso/dsm/powerkey/dbus_action4" "variant:string:event4" || :
dbus-send --system --type=method_call --dest=com.nokia.mce /com/nokia/mce/request com.nokia.mce.request.set_config "string:/system/osso/dsm/powerkey/dbus_action5" "variant:string:event5" || :
dbus-send --system --type=method_call --dest=com.nokia.mce /com/nokia/mce/request com.nokia.mce.request.set_config "string:/system/osso/dsm/powerkey/dbus_action6" "variant:string:event6" || :
export DBUS_SESSION_BUS_ADDRESS=$DSBA
fi

if /sbin/pidof powermenu2-daemon > /dev/null; then
killall powermenu2-daemon || true
fi

if /sbin/pidof powermenu2-gui > /dev/null; then
killall powermenu2-gui || true
fi

if /sbin/pidof powermenu2-flashlight > /dev/null; then
killall powermenu2-flashlight || true
fi

%post
systemctl-user restart powermenu.service

%pre -n sailfishos-ambience-powermenu2
if [ -d /var/lib/patchmanager/ausmt/patches/sailfishos-ambience-powermenu2 ]; then
/usr/sbin/patchmanager -u sailfishos-ambience-powermenu2 || true
fi

%preun -n sailfishos-ambience-powermenu2
if [ -d /var/lib/patchmanager/ausmt/patches/sailfishos-ambience-powermenu2 ]; then
/usr/sbin/patchmanager -u sailfishos-ambience-powermenu2 || true
fi

%files
%attr(4755, root, root) %{_bindir}/powermenu2-daemon
%attr(4755, root, root) %{_bindir}/powermenu2-flashlight
%attr(0755, root, root) %{_bindir}/powermenu2-gui
%defattr(644,root,root,-)
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/86x86/apps/%{name}.png
%{_datadir}/powermenu2
%{_datadir}/dbus-1/services/org.coderus.powermenu.service
%{_datadir}/dbus-1/services/org.coderus.powermenu.flashlight.service
%{_libdir}/libpowermenutools.so
%{_libdir}/qt5/qml/org/coderus/powermenu
%{_libdir}/systemd/user/*.service
%{_libdir}/systemd/user/post-user-session.target.wants/*.service
%{_datadir}/lipstick/quickactions/org.coderus.powermenu.conf

%files -n sailfishos-ambience-powermenu2
%defattr(644,root,root,-)
%{_datadir}/patchmanager/patches/sailfishos-ambience-powermenu2

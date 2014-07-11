%define beta %{nil}
%define scmrev %{nil}

Name: fcitx-mozc
Version: 1.13.1651.102.1
%if "%{beta}" == ""
%if "%{scmrev}" == ""
Release: 3
Source0: http://fcitx.googlecode.com/files/fcitx-mozc-%version.tar.xz
%else
Release: 0.%{scmrev}.1
Source0: %{name}-%{scmrev}.tar.xz
%endif
%else
%if "%{scmrev}" == ""
Release: 0.%{beta}.1
Source0: %{name}-%{version}%{beta}.tar.bz2
%else
Release: 0.%{beta}.0.%{scmrev}.1
Source0: %{name}-%{scmrev}.tar.xz
%endif
%endif
Source1: http://downloads.sourceforge.net/project/pnsft-aur/mozc/ken_all-201305.zip
Source2: http://downloads.sourceforge.net/project/pnsft-aur/mozc/jigyosyo-201305.zip
Source10: %name.rpmlintrc
Summary: Japanese input support for fcitx
URL: http://fcitx.googlecode.com/
License: GPLv2
Group: System/Internationalization
BuildRequires: cmake
BuildRequires: gyp
BuildRequires: pkgconfig(protobuf)
BuildRequires: pkgconfig(fcitx)
BuildRequires: pkgconfig(ibus-1.0)
BuildRequires: pkgconfig(zinnia)
BuildRequires: pkgconfig(QtCore)
BuildRequires: pkgconfig(QtGui)
BuildRequires: pkgconfig(xt)
BuildRequires: pkgconfig(xi)
BuildRequires: pkgconfig(xcursor)
BuildRequires: pkgconfig(gtk+-2.0)
Requires: fcitx

%track
prog %{name} = {
	url = http://code.google.com/p/fcitx/downloads/list
	regex = "%name-(__VER__)\.tar\.xz"
	version = %{version}
}

%description
Japanese input support for fcitx

%prep
%if "%{scmrev}" == ""
%setup -q -n %{name}-%{version}%{beta} -a 1 -a 2
%else
%setup -q -n %{name}
%endif
python dictionary/gen_zip_code_seed.py --zip_code=KEN_ALL.CSV --jigyosyo=JIGYOSYO.CSV >>dictionary/dictionary09.txt

%build
J="`getconf _NPROCESSORS_ONLN`"; [ -z "$J" ] && J=4
GYP_DEFINES="use_libprotobuf=1" ./build_mozc.py gyp --gypdir=%{_bindir} --channel_dev=0
./build_mozc.py build_tools -c Release --jobs=$J
./build_mozc.py build -c Release server/server.gyp:mozc_server gui/gui.gyp:mozc_tool unix/fcitx/fcitx.gyp:fcitx-mozc --jobs=$J
# Workaround for mozc_tool and mozc_server getting the same build-id
%__strip --strip-unneeded out_*/*/mozc_server

%install
for mo in out_*/*/obj/gen/unix/fcitx/po/*.mo; do
	file=`basename $mo`
	lang=${file/.mo/}
	install -D -m 644 $mo %buildroot%_datadir/locale/$lang/LC_MESSAGES/%name.mo
done
install -D -m 755 out_*/*/mozc_server %buildroot%_libdir/mozc/mozc_server
install    -m 755 out_*/*/mozc_tool %buildroot%_libdir/mozc/mozc_tool
install -d -m 755 %buildroot%_libdir/mozc/documents/
install    -m 644 data/installer/*.html %buildroot%_libdir/mozc/documents
install -D -m 755 out_*/*/fcitx-mozc.so %buildroot%_libdir/fcitx/fcitx-mozc.so
install -D -m 644 unix/fcitx/fcitx-mozc.conf %buildroot%_datadir/fcitx/addon/fcitx-mozc.conf
install -D -m 644 unix/fcitx/mozc.conf %buildroot%_datadir/fcitx/inputmethod/mozc.conf
install -D -m 644 data/images/product_icon_32bpp-128.png %buildroot%_datadir/fcitx/mozc/icon/mozc.png
install    -m 644 data/images/unix/ui-alpha_full.png %buildroot%_datadir/fcitx/mozc/icon/mozc-alpha_full.png
install    -m 644 data/images/unix/ui-alpha_half.png %buildroot%_datadir/fcitx/mozc/icon/mozc-alpha_half.png
install    -m 644 data/images/unix/ui-direct.png %buildroot%_datadir/fcitx/mozc/icon/mozc-direct.png
install    -m 644 data/images/unix/ui-hiragana.png %buildroot%_datadir/fcitx/mozc/icon/mozc-hiragana.png
install    -m 644 data/images/unix/ui-katakana_full.png %buildroot%_datadir/fcitx/mozc/icon/mozc-katakana_full.png
install    -m 644 data/images/unix/ui-katakana_half.png %buildroot%_datadir/fcitx/mozc/icon/mozc-katakana_half.png
install    -m 644 data/images/unix/ui-dictionary.png %buildroot%_datadir/fcitx/mozc/icon/mozc-dictionary.png
install    -m 644 data/images/unix/ui-properties.png %buildroot%_datadir/fcitx/mozc/icon/mozc-properties.png
install    -m 644 data/images/unix/ui-tool.png %buildroot%_datadir/fcitx/mozc/icon/mozc-tool.png

%find_lang %name

%files -f %name.lang
%_libdir/mozc
%_libdir/fcitx/fcitx-mozc.so
%_datadir/fcitx/addon/*
%_datadir/fcitx/inputmethod/mozc.conf
%_datadir/fcitx/mozc

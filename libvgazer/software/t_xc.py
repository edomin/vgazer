data = {
    "tinyfiledialogs": {
        "type": "library",
        "platform": "target",
        "projects": [
            {
                "fallback": True,
                "arch": ["any"],
                "os": ["any"],
                "osVersion": ["any"],
                "abi": ["any"],
                "license": ["zlib"],
                "changelog": "https://sourceforge.net/p/tinyfiledialogs/activity/?page=0&limit=100#65c79b2c7e19948b1b33b56a",
                "prereqs": [
                    "{triplet}-gcc",
                ],
                "checker": {
                    "type": "git",
                    "url": "https://git.code.sf.net/p/tinyfiledialogs/code",
                    "files": ["README.txt"],
                    "hint": r'tiny file dialogs \( cross-platform C C\+\+ \) v\d\.\d+(?:\.\d)?',
                },
                "installer": {
                    "type": "custom",
                    "name": "tinyfiledialogs",
                },
            },
        ],
    },
    "unzip": {
        "platform": "host",
        "projects": [
            {
                "arch": ["any"],
                "os": ["archlinux"],
                "osVersion": ["latest"],
                "abi": ["any"],
                "changelog": "https://infozip.sourceforge.net/UnZip.html#Release",
                "checker": {
                    "type": "pacman",
                    "package": "unzip",
                },
                "installer": {
                    "type": "pacman",
                    "package": "unzip",
                },
            },
            {
                "arch": ["any"],
                "os": ["debian"],
                "osVersion": ["any"],
                "abi": ["any"],
                "changelog": "https://infozip.sourceforge.net/UnZip.html#Release",
                "checker": {
                    "type": "apt-cache",
                    "package": "unzip",
                },
                "installer": {
                    "type": "apt",
                    "package": "unzip",
                },
            },
            {
                "arch": ["any"],
                "os": ["steamrt"],
                "osVersion": ["any"],
                "abi": ["any"],
                "changelog": "https://infozip.sourceforge.net/UnZip.html#Release",
                "checker": {
                    "type": "apt-cache",
                    "package": "unzip",
                },
                "installer": {
                    "type": "apt",
                    "package": "unzip",
                },
            },
        ],
    },
    "wayland-libs": {
        "platform": "target",
        "projects": [
            {
                "fallback": True,
                "arch": ["any"],
                "os": ["any"],
                "osVersion": ["any"],
                "abi": ["any"],
                "license": ["mit"],
                "changelog": "https://wayland.freedesktop.org/releases.html",
                "prereqs": [
                    "{triplet}-g++",
                    "{triplet}-gcc",
                    "{triplet}-pkg-config",
                    "libffi",
                    "meson",
                    "wayland-scanner",
                ],
                "checker": {
                    "type": "git",
                    "url": "https://gitlab.freedesktop.org/wayland/wayland.git",
                },
                "installer": {
                    "type": "custom",
                    "name": "wayland",
                },
            },
            {
                "arch": ["any"],
                "os": ["archlinux"],
                "osVersion": ["latest"],
                "abi": ["any"],
                "license": ["mit"],
                "changelog": "https://wayland.freedesktop.org/releases.html",
                "checker": {
                    "type": "pacman",
                    "package": "wayland",
                },
                "installer": {
                    "type": "pacman",
                    "package": "wayland",
                },
            },
            {
                "arch": ["any"],
                "os": ["debian"],
                "osVersion": ["any"],
                "abi": ["any"],
                "license": ["mit"],
                "changelog": "https://wayland.freedesktop.org/releases.html",
                "checker": {
                    "type": "apt-cache",
                    "package": "libwayland-egl-backend-dev",
                },
                "installer": {
                    "type": "apt",
                    "package": [
                        "libwayland-dev",
                        "libwayland-egl-backend-dev"
                    ],
                },
            },
            {
                "arch": ["any"],
                "os": ["steamrt"],
                "osVersion": ["any"],
                "abi": ["gnu"],
                "license": ["mit"],
                "changelog": "https://wayland.freedesktop.org/releases.html",
                "checker": {
                    "type": "apt-cache",
                    "package": "libwayland-egl-backend-dev",
                },
                "installer": {
                    "type": "not-needed",
                },
            },
        ],
    },
    "wayland-scanner": {
        "platform": "host",
        "projects": [
            {
                "fallback": True,
                "arch": ["any"],
                "os": ["any"],
                "osVersion": ["any"],
                "abi": ["any"],
                "license": ["mit"],
                "changelog": "https://wayland.freedesktop.org/releases.html",
                "prereqs": [
                    "gcc",
                    "meson",
                    "pkg-config",
                ],
                "checker": {
                    "type": "git",
                    "url": "https://gitlab.freedesktop.org/wayland/wayland.git",
                },
                "installer": {
                    "type": "custom",
                    "name": "wayland-scanner",
                },
            },
            {
                "arch": ["any"],
                "os": ["archlinux"],
                "osVersion": ["latest"],
                "abi": ["any"],
                "license": ["mit"],
                "changelog": "https://wayland.freedesktop.org/releases.html",
                "checker": {
                    "type": "pacman",
                    "package": "wayland",
                },
                "installer": {
                    "type": "pacman",
                    "package": "wayland",
                },
            },
            # >= 1.22.0 required for build wayland-libs
            {
                "arch": ["any"],
                "os": ["debian"],
                "osVersion": ["trixie", "sid"],
                "abi": ["any"],
                "license": ["mit"],
                "changelog": "https://wayland.freedesktop.org/releases.html",
                "checker": {
                    "type": "apt-cache",
                    "package": "libwayland-bin",
                },
                "installer": {
                    "type": "apt",
                    "package": "libwayland-bin",
                },
            },
            {
                "arch": ["any"],
                "os": ["steamrt"],
                "osVersion": ["any"],
                "abi": ["any"],
                "changelog": "https://wayland.freedesktop.org/releases.html",
                "checker": {
                    "type": "apt-cache",
                    "package": "libwayland-bin",
                },
                "installer": {
                    "type": "not-needed",
                },
            },
        ],
    },
    "wget": {
        "platform": "host",
        "projects": [
            {
                "arch": ["any"],
                "os": ["archlinux"],
                "osVersion": ["latest"],
                "abi": ["any"],
                "changelog": "https://savannah.gnu.org/news/?group=wget",
                "checker": {
                    "type": "pacman",
                    "package": "wget",
                },
                "installer": {
                    "type": "pacman",
                    "package": "wget",
                },
            },
            {
                "arch": ["any"],
                "os": ["debian"],
                "osVersion": ["any"],
                "abi": ["any"],
                "changelog": "https://savannah.gnu.org/news/?group=wget",
                "checker": {
                    "type": "apt-cache",
                    "package": "wget",
                },
                "installer": {
                    "type": "apt",
                    "package": "wget",
                },
            },
            {
                "arch": ["any"],
                "os": ["steamrt"],
                "osVersion": ["any"],
                "abi": ["any"],
                "changelog": "https://savannah.gnu.org/news/?group=wget",
                "checker": {
                    "type": "apt-cache",
                    "package": "wget",
                },
                "installer": {
                    "type": "not-needed",
                },
            },
        ],
    },
    "x86_64-linux-gnu-g++": {
        "platform": "host",
        "projects": [
            {
                "arch": ["x86_64"],
                "os": ["archlinux"],
                "osVersion": ["any"],
                "abi": ["any"],
                "changelog": "https://gcc.gnu.org/",
                "prereqs": ["g++"],
                "checker": {
                    "type": "pacman",
                    "package": "gcc",
                },
                "installer": {
                    "type": "not-needed",
                },
            },
            {
                "arch": ["x86_64"],
                "os": ["debian"],
                "osVersion": ["any"],
                "abi": ["any"],
                "changelog": "https://gcc.gnu.org/",
                "checker": {
                    "type": "apt-cache",
                    "package": "g++",
                },
                "installer": {
                    "type": "not-needed",
                },
            },
            {
                "arch": ["any"],
                "os": ["steamrt"],
                "osVersion": ["any"],
                "abi": ["any"],
                "changelog": "https://gcc.gnu.org/",
                "prereqs": [
                    "gcc",
                ],
                "checker": {
                    "type": "apt-cache",
                    "package": "gcc-12-monolithic",
                },
                "installer": {
                    "type": "cmd",
                    "cmds": [
                        [
                            "update-alternatives", "--set",
                            "x86_64-linux-gnu-g++", "/usr/bin/g++-12", "1"
                        ],
                    ],
                },
            },
        ],
    },
    "x86_64-linux-gnu-gcc": {
        "platform": "host",
        "projects": [
            {
                "arch": ["x86_64"],
                "os": ["archlinux"],
                "osVersion": ["any"],
                "abi": ["any"],
                "changelog": "https://gcc.gnu.org/",
                "prereqs": ["gcc"],
                "checker": {
                    "type": "pacman",
                    "package": "gcc",
                },
                "installer": {
                    "type": "not-needed",
                },
            },
            {
                "arch": ["x86_64"],
                "os": ["debian"],
                "osVersion": ["any"],
                "abi": ["any"],
                "changelog": "https://gcc.gnu.org/",
                "checker": {
                    "type": "apt-cache",
                    "package": "gcc",
                },
                "installer": {
                    "type": "not-needed",
                },
            },
            {
                "arch": ["any"],
                "os": ["steamrt"],
                "osVersion": ["any"],
                "abi": ["any"],
                "changelog": "https://gcc.gnu.org/",
                "checker": {
                    "type": "apt-cache",
                    "package": "gcc-12-monolithic",
                },
                "installer": {
                    "type": "cmd",
                    "cmds": [
                        [
                            "update-alternatives", "--set",
                            "x86_64-linux-gnu-cpp", "/usr/bin/cpp-12", "1"
                        ],
                        [
                            "update-alternatives", "--set",
                            "x86_64-linux-gnu-gcc", "/usr/bin/gcc-12", "1"
                        ],
                        [
                            "update-alternatives", "--set",
                            "x86_64-linux-gnu-gcc-ar", "/usr/bin/gcc-ar-12",
                            "1"
                        ],
                        [
                            "update-alternatives", "--set",
                            "x86_64-linux-gnu-gcc-nm", "/usr/bin/gcc-nm-12",
                            "1"
                        ],
                        [
                            "update-alternatives", "--set",
                            "x86_64-linux-gnu-gcc-ranlib",
                            "/usr/bin/gcc-ranlib-12", "1"
                        ],
                        [
                            "update-alternatives", "--set",
                            "x86_64-linux-gnu-gcov", "/usr/bin/gcov-12", "1"
                        ]
                    ],
                },
            },
        ],
    },
    "x86_64-linux-gnu-pkg-config": {
        "platform": "host",
        "projects": [
            {
                "arch": ["any"],
                "os": ["archlinux"],
                "osVersion": ["latest"],
                "abi": ["gnu"],
                "changelog": "https://gitlab.freedesktop.org/pkg-config/pkg-config/-/blob/master/NEWS?ref_type=heads",
                "prereqs": [
                    "pkg-config",
                ],
                "checker": {
                    "type": "pacman",
                    "package": "pkg-config",
                },
                "installer": {
                    "type": "pkg-config",
                    "triplet": "x86_64-linux-gnu",
                },
            },
            {
                "arch": ["any"],
                "os": ["debian"],
                "osVersion": ["any"],
                "abi": ["gnu"],
                "changelog": "https://gitlab.freedesktop.org/pkg-config/pkg-config/-/blob/master/NEWS?ref_type=heads",
                "prereqs": [
                    "pkg-config",
                ],
                "checker": {
                    "type": "apt-cache",
                    "package": "pkg-config",
                },
                "installer": {
                    "type": "pkg-config",
                    "triplet": "x86_64-linux-gnu",
                },
            },
            {
                "arch": ["any"],
                "os": ["steamrt"],
                "osVersion": ["any"],
                "abi": ["any"],
                "prereqs": [
                    "pkg-config",
                ],
                "checker": {
                    "type": "apt-cache",
                    "package": "pkg-config",
                },
                "installer": {
                    "type": "pkg-config",
                    "triplet": "x86_64-linux-gnu",
                },
            },
        ],
    },
    "x86_64-w64-mingw32-g++": {
        "platform": "host",
        "projects": [
            {
                "arch": ["any"],
                "os": ["archlinux"],
                "osVersion": ["latest"],
                "abi": ["any"],
                "changelog": "https://www.mingw-w64.org/changelog/",
                "prereqs": ["x86_64-w64-mingw32-gcc"],
                "checker": {
                    "type": "pacman",
                    "package": "mingw-w64-gcc",
                },
                "installer": {
                    "type": "not-needed",
                },
            },
            {
                "arch": ["any"],
                "os": ["debian"],
                "osVersion": ["buster"],
                "abi": ["any"],
                "changelog": "https://www.mingw-w64.org/changelog/",
                "prereqs": [
                    "x86_64-w64-mingw32-gcc",
                ],
                "checker": {
                    "type": "apt-cache",
                    "package": "g++-mingw-w64-x86-64",
                },
                "installer": {
                    "type": "apt",
                    "package": "gcc-mingw-w64-x86-64",
                    "cmds": [
                        [
                            "update-alternatives", "--set",
                            "x86_64-w64-mingw32-g++",
                            "/usr/bin/x86_64-w64-mingw32-g++-posix"
                        ],
                    ],
                },
            },
            {
                "arch": ["any"],
                "os": ["debian"],
                "osVersion": ["bullseye", "bookworm", "trixie", "sid"],
                "abi": ["any"],
                "changelog": "https://www.mingw-w64.org/changelog/",
                "prereqs": [
                    "x86_64-w64-mingw32-gcc",
                ],
                "checker": {
                    "type": "apt-cache",
                    "package": "g++-mingw-w64-x86-64-posix",
                },
                "installer": {
                    "type": "apt",
                    "package": "gcc-mingw-w64-x86-64-posix",
                    "cmds": [
                        [
                            "update-alternatives", "--set",
                            "x86_64-w64-mingw32-g++",
                            "/usr/bin/x86_64-w64-mingw32-g++-posix"
                        ],
                    ],
                },
            },
        ],
    },
    "x86_64-w64-mingw32-gcc": {
        "platform": "host",
        "projects": [
            {
                "arch": ["any"],
                "os": ["archlinux"],
                "osVersion": ["latest"],
                "abi": ["any"],
                "changelog": "https://www.mingw-w64.org/changelog/",
                "checker": {
                    "type": "pacman",
                    "package": "mingw-w64-gcc",
                },
                "installer": {
                    "type": "pacman",
                    "package": "mingw-w64-gcc",
                },
            },
            {
                "arch": ["any"],
                "os": ["debian"],
                "osVersion": ["buster"],
                "abi": ["any"],
                "changelog": "https://www.mingw-w64.org/changelog/",
                "checker": {
                    "type": "apt-cache",
                    "package": "gcc-mingw-w64-x86-64",
                },
                "installer": {
                    "type": "apt",
                    "package": "gcc-mingw-w64-x86-64",
                    "postInstallCommands": [
                        ["update-alternatives", "--set",
                         "x86_64-w64-mingw32-gcc",
                         "/usr/bin/x86_64-w64-mingw32-gcc-posix"],
                    ],
                },
            },
            {
                "arch": ["any"],
                "os": ["debian"],
                "osVersion": ["bullseye", "bookworm", "trixie", "sid"],
                "abi": ["any"],
                "changelog": "https://www.mingw-w64.org/changelog/",
                "checker": {
                    "type": "apt-cache",
                    "package": "gcc-mingw-w64-x86-64-posix",
                },
                "installer": {
                    "type": "apt",
                    "package": "gcc-mingw-w64-x86-64-posix",
                    "postInstallCommands": [
                        ["update-alternatives", "--set",
                         "x86_64-w64-mingw32-gcc",
                         "/usr/bin/x86_64-w64-mingw32-gcc-posix"],
                    ],
                },
            },
        ],
    },
    "x86_64-w64-mingw32-pkg-config": {
        "platform": "host",
        "projects": [
            {
                "arch": ["any"],
                "os": ["archlinux"],
                "osVersion": ["latest"],
                "abi": ["gnu"],
                "changelog": "https://gitlab.freedesktop.org/pkg-config/pkg-config/-/blob/master/NEWS?ref_type=heads",
                "prereqs": [
                    "pkg-config",
                ],
                "checker": {
                    "type": "pacman",
                    "package": "pkgconf",
                },
                "installer": {
                    "type": "pkg-config",
                    "triplet": "x86_64-w64-mingw32",
                },
            },
            {
                "arch": ["any"],
                "os": ["debian"],
                "osVersion": ["any"],
                "abi": ["gnu"],
                "changelog": "https://gitlab.freedesktop.org/pkg-config/pkg-config/-/blob/master/NEWS?ref_type=heads",
                "prereqs": [
                    "pkg-config",
                ],
                "checker": {
                    "type": "apt-cache",
                    "package": "pkg-config",
                },
                "installer": {
                    "type": "pkg-config",
                    "triplet": "x86_64-w64-mingw32",
                },
            },
        ],
    },
    "xau": {
        "platform": "target",
        "projects": [
            {
                "fallback": True,
                "arch": ["any"],
                "os": ["any"],
                "osVersion": ["any"],
                "abi": ["any"],
                "license": ["mit"],
                "changelog": "https://gitlab.freedesktop.org/xorg/lib/libxau/-/tags",
                "prereqs": [
                    "{triplet}-gcc",
                    "{triplet}-pkg-config",
                    "autoconf",
                    "libtool",
                    "make",
                    "xorg-macros",
                    "xorgproto",
                ],
                "checker": {
                    "type": "git",
                    "url": "https://gitlab.freedesktop.org/xorg/lib/libxau.git",
                    "hint": r'libXau-\d\.\d\.\d+',
                },
                "installer": {
                    "type": "custom",
                    "name": "xau",
                    "fallback": {
                        "type": "custom",
                        "name": "xau-github",
                    },
                },
            },
            {
                "arch": ["any"],
                "os": ["archlinux"],
                "osVersion": ["latest"],
                "abi": ["gnu"],
                "license": ["mit"],
                "changelog": "https://gitlab.freedesktop.org/xorg/lib/libxau/-/tags",
                "checker": {
                    "type": "pacman",
                    "package": "libxau",
                },
                "installer": {
                    "type": "pacman",
                    "package": "libxau",
                },
            },
            {
                "arch": ["any"],
                "os": ["debian"],
                "osVersion": ["any"],
                "abi": ["gnu"],
                "license": ["mit"],
                "changelog": "https://gitlab.freedesktop.org/xorg/lib/libxau/-/tags",
                "checker": {
                    "type": "apt-cache",
                    "package": "libxau-dev",
                },
                "installer": {
                    "type": "apt",
                    "package": "libxau-dev",
                },
            },
            {
                "arch": ["any"],
                "os": ["steamrt"],
                "osVersion": ["any"],
                "abi": ["gnu"],
                "license": ["mit"],
                "changelog": "https://gitlab.freedesktop.org/xorg/lib/libxau/-/tags",
                "checker": {
                    "type": "apt-cache",
                    "package": "libxau-dev",
                },
                "installer": {
                    "type": "not-needed",
                },
            },
        ],
    },
    "xcb": {
        "platform": "target",
        "projects": [
            {
                "fallback": True,
                "arch": ["any"],
                "os": ["any"],
                "osVersion": ["any"],
                "abi": ["any"],
                "license": ["x11"],
                "changelog": "https://xcb.freedesktop.org/",
                "prereqs": [
                    "{triplet}-gcc",
                    "{triplet}-pkg-config",
                    "autoconf",
                    "make",
                    "pthread-stubs",
                    "wget",
                    "xcb-proto",
                    "xau",
                ],
                "checker": {
                    "type": "git",
                    "url": "https://gitlab.freedesktop.org/xorg/lib/libxcb.git",
                },
                "installer": {
                    "type": "custom",
                    "name": "xcb",
                },
            },
            {
                "arch": ["any"],
                "os": ["archlinux"],
                "osVersion": ["latest"],
                "abi": ["gnu"],
                "license": ["x11"],
                "changelog": "https://xcb.freedesktop.org/",
                "checker": {
                    "type": "pacman",
                    "package": "libxcb",
                },
                "installer": {
                    "type": "pacman",
                    "package": "libxcb",
                },
            },
            {
                "arch": ["any"],
                "os": ["debian"],
                "osVersion": ["any"],
                "abi": ["gnu"],
                "license": ["x11"],
                "changelog": "https://xcb.freedesktop.org/",
                "checker": {
                    "type": "apt-cache",
                    "package": "libx11-xcb-dev",
                },
                "installer": {
                    "type": "apt",
                    "package": "libx11-xcb-dev",
                },
            },
            {
                "arch": ["any"],
                "os": ["steamrt"],
                "osVersion": ["any"],
                "abi": ["gnu"],
                "license": ["x11"],
                "changelog": "https://xcb.freedesktop.org/",
                "checker": {
                    "type": "apt-cache",
                    "package": "libx11-xcb-dev",
                },
                "installer": {
                    "type": "not-needed",
                },
            },
        ],
    },
    "xcb-proto": {
        "platform": "target",
        "projects": [
            {
                "fallback": True,
                "arch": ["any"],
                "os": ["any"],
                "osVersion": ["any"],
                "abi": ["any"],
                "license": ["x11"],
                "changelog": "https://xcb.freedesktop.org/",
                "prereqs": [
                    "autoconf",
                    "automake",
                    "make",
                ],
                "checker": {
                    "type": "git",
                    "url": "https://gitlab.freedesktop.org/xorg/proto/xcbproto.git",
                },
                "installer": {
                    "type": "custom",
                    "name": "xcb-proto",
                },
            },
            {
                "arch": ["any"],
                "os": ["archlinux"],
                "osVersion": ["latest"],
                "abi": ["gnu"],
                "license": ["x11"],
                "changelog": "https://xcb.freedesktop.org/",
                "checker": {
                    "type": "pacman",
                    "package": "xcb-proto",
                },
                "installer": {
                    "type": "pacman",
                    "package": "xcb-proto",
                },
            },
            {
                "arch": ["any"],
                "os": ["debian"],
                "osVersion": ["any"],
                "abi": ["gnu"],
                "license": ["x11"],
                "changelog": "https://xcb.freedesktop.org/",
                "checker": {
                    "type": "apt-cache",
                    "package": "xcb-proto",
                },
                "installer": {
                    "type": "apt",
                    "package": "xcb-proto",
                },
            },
            {
                "arch": ["any"],
                "os": ["steamrt"],
                "osVersion": ["any"],
                "abi": ["gnu"],
                "license": ["x11"],
                "changelog": "https://xcb.freedesktop.org/",
                "checker": {
                    "type": "apt-cache",
                    "package": "xcb-proto",
                },
                "installer": {
                    "type": "not-needed",
                },
            },
        ],
    },
}

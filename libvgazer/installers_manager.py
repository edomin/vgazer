from libvgazer.exceptions         import UnknownInstaller
from libvgazer.install.apt        import InstallApt
from libvgazer.install.cmd        import InstallCmd
from libvgazer.install.pip        import InstallPip
from libvgazer.install.pip3       import InstallPip3
from libvgazer.install.pkg_config import InstallPkgConfig

class InstallersManager:
    def __init__(self):
        self.installFuncs = {
            "apt": lambda software, platformData, installerData, mirrors,
             verbose:
                InstallApt(software, installerData["package"],
                 installerData["postInstallCommands"] if "postInstallCommands"
                  in installerData else None,
                 platformData["host"],
                 verbose),
            "cmd": lambda software, platformData, installerData, mirrors,
             verbose:
                InstallCmd(software, installerData["cmds"], verbose),
            "not-needed": lambda software, platformData, installerData,
             mirrors, verbose:
                True,
            "pip": lambda software, platformData, installerData, mirrors,
             verbose:
                InstallPip(software, installerData["package"], verbose),
            "pip3": lambda software, platformData, installerData,
             mirrors, verbose:
                InstallPip3(software, installerData["package"], verbose),
            "pkg-config": lambda software, platformData, installerData,
             mirrors, verbose:
                InstallPkgConfig(software, installerData["triplet"],
                 platformData, verbose),
        }

    def GetInstallFunc(self, installerType):
        if installerType in self.installFuncs:
            return self.installFuncs[installerType]
        else:
            raise UnknownInstaller(
             "Unknown installer: " + installerType)

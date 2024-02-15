from multimethod import multimethod
import re

from libvgazer.auth.base           import AuthBase
from libvgazer.checkers_manager    import CheckersManager
from libvgazer.exceptions          import CompatibleProjectNotFound
from libvgazer.exceptions          import InstallError
from libvgazer.exceptions          import UnknownSoftware
from libvgazer.exceptions          import VersionCheckError
from libvgazer.install.custom      import InstallCustom
from libvgazer.installers_manager  import InstallersManager
from libvgazer.mirrors.gnu         import MirrorsGnu
from libvgazer.mirrors.sourceforge import MirrorsSourceforge
from libvgazer.mirrors.xorg        import MirrorsXorg
from libvgazer.platform            import GetGenericTriplet
from libvgazer.platform            import Platform
from libvgazer.software            import SoftwareData
from libvgazer.version.custom      import VersionCustom

class Vgazer:
    def __init__(self, arch=None, os=None, osVersion=None, abi=None,
     customCheckers={}, customInstallers={}, customSoftwareData={},
     supportOnly=False):
        if not supportOnly:
            self.auth = {
                "base": AuthBase(),
            }
            self.versionCustom = VersionCustom(self.auth["base"],
             customCheckers)
            self.checkersManager = CheckersManager()
            self.installersManager = InstallersManager()
            self.mirrors = {
                "gnu": MirrorsGnu(),
                "sourceforge": MirrorsSourceforge(),
                "xorg": MirrorsXorg(),
            }
            self.installCustom = InstallCustom(customInstallers)
            self.installedSoftware = []
        self.softwareData = SoftwareData(customSoftwareData)
        self.platform = {
            "host":   Platform(),
            "target": Platform(arch, os, osVersion, abi),
        }

    def GetHostPlatform(self):
        return self.platform["host"]

    def GetTargetPlatform(self):
        return self.platform["target"]

    def GetSoftwareData(self):
        return self.softwareData

    @multimethod
    def ChooseProject(self, projects: list, platformData: Platform):
        maxRatingProject = None
        maxRating = Platform.COMP_INCOMPATIBLE
        for project in projects:
            projectRating = platformData.GetCompatibilityRating(project["arch"],
             project["os"], project["osVersion"], project["abi"])
            if projectRating > maxRating:
                maxRating = projectRating
                maxRatingProject = project
        if maxRating >= Platform.COMP_COMPATIBLE:
            return maxRatingProject
        else:
            return None

    @multimethod
    def ChooseProject(self, softwareData: dict):
        return self.ChooseProject(softwareData["projects"],
         self.platform[softwareData["platform"]])

    def SearchFallbackProject(self, projects):
        for project in projects:
            if "fallback" in project:
                return project

        return None

    def NormalizeVersion(self, version):
        normalized = version.split(":")[1] if ":" in version else version
        normalized = re.sub(r'^\D(?:\D*[a-z])?[a-zA-Z]?(?:\d*\-)?' , "" ,
         normalized)
        normalized = re.sub(r'\.\D*$' , "" , normalized)
        splitted = re.split(r'[\.\-\:\s]', normalized)

        if len(splitted) > 4:
            return ".".join(splitted[0:4]) + "".join(splitted[4:])

        return ".".join(splitted)

    def UseChecker(self, software, checker):
        softwareData = self.softwareData.GetData()
        softwarePlatform = softwareData[software]["platform"]

        try:
            if checker["type"] == "custom":
                return self.versionCustom.Check(checker["name"], self.mirrors)
            else:
                checkFunc = self.checkersManager.GetCheckFunc(checker["type"])
                return checkFunc(self.auth, self.platform[softwarePlatform],
                 checker)

        except VersionCheckError as versionCheckError:
            if "fallback" in checker:
                return self.UseChecker(software, checker["fallback"])
            else:
                raise versionCheckError

    def CheckVersion(self, software):
        softwareData = self.softwareData.GetData()
        if software not in softwareData:
            raise UnknownSoftware("Unknown software: {software}".format(
             software=software))

        project = self.ChooseProject(softwareData[software])
        if project is None:
            raise CompatibleProjectNotFound(
             "Unable to find compatible project for software: "
             "{software}".format(software=software))

        checker = project["checker"]

        return self.NormalizeVersion(self.UseChecker(software, checker))

    def VersionsList(self, softwareList):
        result = []
        for software in softwareList:
            result.append({
                "software": software,
                "version": self.CheckVersion(software)
            })
        return result

    def UseInstaller(self, software, installer, verbose):
        softwareData = self.softwareData.GetData()
        softwarePlatform = softwareData[software]["platform"]

        if software in self.installedSoftware:
            return

        try:
            if installer["type"] == "custom":
                self.installCustom.Install(software, installer["name"],
                 softwarePlatform, self.platform, self.mirrors, verbose)
            else:
                installFunc = self.installersManager.GetInstallFunc(
                 installer["type"])
                installFunc(software, self.platform, installer, self.mirrors,
                 verbose)
            self.installedSoftware.append(software)
        except InstallError as installError:
            raise installError

    def InstallProject(self, software, project, verbose):
        prereqs = project["prereqs"] if "prereqs" in project else []

        for prereq in prereqs:
            prereq = prereq.format(
             hostTriplet=GetGenericTriplet(self.platform["host"]),
             triplet=GetGenericTriplet(self.platform["target"]),
             arch=self.platform["target"].GetArch())
            if prereq not in self.installedSoftware:
                self.Install(prereq, verbose)

        installer = project["installer"]

        try:
            self.UseInstaller(software, installer, verbose)
        except InstallError as installError:
            fallbackProject = self.SearchFallbackProject(softwareProjects);
            if (fallbackProject is not None and fallbackProject is not project):
                print(
                 "VGAZER: Something went wrong. Starting fallback installation "
                 "steps"
                )
                self.InstallProject(software, fallbackProject, verbose)
            else:
                raise installError

    def Install(self, software, verbose=False):
        if software in self.installedSoftware:
            return

        softwareData = self.softwareData.GetData()
        if software not in softwareData:
            raise UnknownSoftware("Unknown software: " + software)

        project = self.ChooseProject(softwareData[software])
        if project is None:
            raise CompatibleProjectNotFound(
             "Unable to find compatible project for software: " + software)

        self.InstallProject(software, project, verbose)

    def InstallList(self, softwareList, verbose=False):
        for software in softwareList:
            self.Install(software, verbose)

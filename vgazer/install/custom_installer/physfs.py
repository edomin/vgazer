import os
import requests
from bs4 import BeautifulSoup

from vgazer.command         import GetCommandOutputUtf8
from vgazer.command         import RunCommand
from vgazer.config.cmake    import ConfigCmake
from vgazer.exceptions      import CommandError
from vgazer.exceptions      import InstallError
from vgazer.platform        import GetInstallPrefix
from vgazer.store.temp      import StoreTemp
from vgazer.working_dir     import WorkingDir

def GetTarballUrl(auth):
    response = requests.get(
     "https://icculus.org/physfs/downloads/LATEST_VERSION.html")
    html = response.content.decode("utf-8")
    parsedHtml = BeautifulSoup(html, "html.parser")

    return ("https://icculus.org/physfs/downloads/"
     + parsedHtml.find_all("a")[0]["href"])

def Install(auth, software, platform, platformData, mirrors, verbose):
    configCmake = ConfigCmake(platformData)
    configCmake.GenerateCrossFile()
    installPrefix = GetInstallPrefix(platformData)

    storeTemp = StoreTemp()
    storeTemp.ResolveEmptySubdirectory(software)
    tempPath = storeTemp.GetSubdirectoryPath(software)

    try:
        tarballUrl = GetTarballUrl(auth)
    except requests.exceptions.ConnectionError:
        raise InstallError(software + " not installed")
    tarballShortFilename = tarballUrl.split("/")[-1]

    try:
        with WorkingDir(tempPath):
            RunCommand(["wget", "-P", "./", tarballUrl], verbose)
            RunCommand(
             ["tar", "--verbose", "--extract", "--bz2", "--file",
              tarballShortFilename],
             verbose)
            output = GetCommandOutputUtf8(
             ["tar", "--list", "--file", tarballShortFilename]
            )
        extractedDir = os.path.join(tempPath,
         output.splitlines()[0].split("/")[0])
        with WorkingDir(extractedDir):
            RunCommand(["mkdir", "build"], verbose)
        buildDir = os.path.join(extractedDir, "build")
        with WorkingDir(buildDir):
            RunCommand(
             ["cmake", "..",
              "-DCMAKE_TOOLCHAIN_FILE=" + configCmake.GetCrossFileName(),
              "-DCMAKE_INSTALL_PREFIX=" + installPrefix,
              "-DPHYSFS_BUILD_SHARED=FALSE", "-DPHYSFS_BUILD_TEST=FALSE",
              "-DCMAKE_VERBOSE_MAKEFILE:BOOL=ON"],
             verbose)
            RunCommand(["make"], verbose)
            RunCommand(["make", "install"], verbose)
    except CommandError:
        print("VGAZER: Unable to install", software)
        raise InstallError(software + " not installed")

    print("VGAZER:", software, "installed")

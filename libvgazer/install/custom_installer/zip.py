import os

from libvgazer.command              import GetCommandOutputUtf8
from libvgazer.command              import RunCommand
from libvgazer.config.cmake         import ConfigCmake
from libvgazer.exceptions           import CommandError
from libvgazer.exceptions           import GithubApiError
from libvgazer.exceptions           import InstallError
from libvgazer.github_api_error_mgr import GithubApiErrorMgr
from libvgazer.platform             import GetInstallPrefix
from libvgazer.store.temp           import StoreTemp
from libvgazer.working_dir          import WorkingDir

def Install(auth, software, platform, platformData, mirrors, verbose):
    configCmake = ConfigCmake(platformData)
    configCmake.GenerateCrossFile()
    crossfile = configCmake.GetCrossFileName()

    installPrefix = GetInstallPrefix(platformData)

    storeTemp = StoreTemp()
    storeTemp.ResolveEmptySubdirectory(software)
    tempPath = storeTemp.GetSubdirectoryPath(software)

    try:
        releases = auth["github"].GetJson(
         "https://api.github.com/repos/kuba--/zip/releases")
    except ConnectionError:
        print("VGAZER: Unable to know last version of", software)
        raise InstallError(
         "{software} not installed".format(software=software))

    with GithubApiErrorMgr(releases, "kuba--/zip") as errMgr:
        if errMgr.IsErrorOccured():
            raise GithubApiError(errMgr.GetErrorText())

    tarballUrl = releases[0]["tarball_url"]
    tarballShortFilename = "zip.tar.gz"

    try:
        with WorkingDir(tempPath):
            RunCommand(
             ["wget", "-P", "./", "-O", tarballShortFilename, tarballUrl],
             verbose)
            RunCommand(
             ["tar", "--verbose", "--extract", "--gzip", "--file",
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
              "-DCMAKE_TOOLCHAIN_FILE={crossfile}".format(crossfile=crossfile),
              "-DCMAKE_INSTALL_PREFIX={prefix}".format(prefix=installPrefix),
              "-DCMAKE_VERBOSE_MAKEFILE:BOOL=ON",
              "-DCMAKE_DISABLE_TESTING=ON"],
             verbose)
            RunCommand(
             ["make", "-j{cores_count}".format(cores_count=os.cpu_count())],
             verbose)
            RunCommand(["make", "install"], verbose)
    except CommandError:
        print("VGAZER: Unable to install", software)
        raise InstallError(
         "{software} not installed".format(software=software))

    print("VGAZER:", software, "installed")

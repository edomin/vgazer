import os

from vgazer.command              import GetCommandOutputUtf8
from vgazer.command              import RunCommand
from vgazer.exceptions           import CommandError
from vgazer.exceptions           import GithubApiError
from vgazer.exceptions           import InstallError
from vgazer.github_api_error_mgr import GithubApiErrorMgr
from vgazer.platform             import GetInstallPrefix
from vgazer.platform             import GetTriplet
from vgazer.store.temp           import StoreTemp
from vgazer.working_dir          import WorkingDir

def Install(auth, software, platform, platformData, mirrors, verbose):
    installPrefix = GetInstallPrefix(platformData)
    triplet = GetTriplet(platformData["target"])

    storeTemp = StoreTemp()
    storeTemp.ResolveEmptySubdirectory(software)
    tempPath = storeTemp.GetSubdirectoryPath(software)

    try:
        releases = auth["github"].GetJson(
         "https://api.github.com/repos/LuaJIT/LuaJIT/releases")
    except ConnectionError:
        print("VGAZER: Unable to know last version of", software)
        raise InstallError(software + " not installed")

    with GithubApiErrorMgr(releases, "LuaJIT/LuaJIT") as errMgr:
        if errMgr.IsErrorOccured():
            raise GithubApiError(errMgr.GetErrorText())

    tarballUrl = releases[0]["tarball_url"]
    tarballShortFilename = tarballUrl.split("/")[-1]

    try:
        with WorkingDir(tempPath):
            RunCommand(["wget", "-P", "./", tarballUrl], verbose)
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
            RunCommand(
             [
              "make", "-j{cores_count}".format(cores_count=os.cpu_count()),
              "BUILDMODE=static",
              "CROSS={triplet}-".format(triplet=triplet),
              "TARGET_SYS={os}".format(
               os=platformData["target"].GetOs().capitalize())
             ],
             verbose)
            RunCommand(
             ["make", "install",
              "PREFIX={prefix}".format(prefix=installPrefix)
             ],
             verbose)
    except CommandError:
        print("VGAZER: Unable to install", software)
        raise InstallError("{software} not installed".format(software=software))

    print("VGAZER:", software, "installed")
import os
import requests

from vgazer.command         import GetCommandOutputUtf8
from vgazer.command         import RunCommand
from vgazer.exceptions      import CommandError
from vgazer.exceptions      import GithubApiRateLimitExceeded
from vgazer.exceptions      import InstallError
from vgazer.github_common   import GithubCheckApiRateLimitExceeded
from vgazer.platform        import GetTempDirectoryPath
from vgazer.store.temp      import StoreTemp
from vgazer.working_dir     import WorkingDir

def Install(auth, software, platform, platformData, verbose):
    if platformData["target"].PlatformsEqual(platformData["host"]):
        installPrefix = "/usr/local"
    else:
        installPrefix = ("/usr/local/" + platformData["target"].GetArch() +
         "-" + platformData["target"].GetOs())

    storeTemp = StoreTemp()
    storeTemp.ResolveDirectory()
    if storeTemp.SubdirectoryExists(software):
        storeTemp.RemoveSubdirectory(software)
    storeTemp.ResolveSubdirectory(software)

    tempPath = storeTemp.GetSubdirectoryPath(software)

    releases = auth["github"].GetJson(
     "https://api.github.com/repos/DaveGamble/cJSON/releases")

    if GithubCheckApiRateLimitExceeded(releases):
        raise GithubApiRateLimitExceeded(
         "Github API rate limit reached while searching last version of "
         "repo: DaveGamble/cJSON"
        )

    tarballUrl = releases[0]["tarball_url"]
    tarballShortFilename = tarballUrl.split("/")[-1]
    #tarballFilename = os.path.join(tempPath, tarballShortFilename)

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
        extractedDir = os.path.join(tempPath, output.splitlines()[0])
        with WorkingDir(extractedDir):
            RunCommand(["mkdir", "build"], verbose)
        buildDir = os.path.join(extractedDir, "build")
        with WorkingDir(buildDir):
            RunCommand(
             ["cmake", "..", '-DCMAKE_C_FLAGS="-fPIC"',
              "-DENABLE_CJSON_TEST=Off", "-DBUILD_SHARED_LIBS=Off",
              "-DCMAKE_INSTALL_PREFIX=" + installPrefix],
             verbose)
            RunCommand(["make"], verbose)
            RunCommand(["make", "install"], verbose)
    except CommandError:
        print("Unable to install", software)
        raise InstallError(software + " not installed")

    print(software, "installed")

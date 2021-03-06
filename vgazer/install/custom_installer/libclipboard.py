import os

from vgazer.command         import GetCommandOutputUtf8
from vgazer.command         import RunCommand
from vgazer.config.cmake    import ConfigCmake
from vgazer.exceptions      import CommandError
from vgazer.exceptions      import GithubApiRateLimitExceeded
from vgazer.exceptions      import InstallError
from vgazer.github_common   import GithubCheckApiRateLimitExceeded
from vgazer.platform        import GetArFullPath
from vgazer.platform        import GetInstallPrefix
from vgazer.store.temp      import StoreTemp
from vgazer.working_dir     import WorkingDir

def Install(auth, software, platform, platformData, mirrors, verbose):
    configCmake = ConfigCmake(platformData)
    configCmake.GenerateCrossFile()
    installPrefix = GetInstallPrefix(platformData)
    ar = GetArFullPath(platformData["target"])

    storeTemp = StoreTemp()
    storeTemp.ResolveEmptySubdirectory(software)
    tempPath = storeTemp.GetSubdirectoryPath(software)

    releases = auth["github"].GetJson(
     "https://api.github.com/repos/jtanx/libclipboard/releases")

    if GithubCheckApiRateLimitExceeded(releases):
        raise GithubApiRateLimitExceeded(
         "Github API rate limit reached while searching last version of "
         "repo: jtanx/libclipboard"
        )

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
            RunCommand(["mkdir", "build"], verbose)
        buildDir = os.path.join(extractedDir, "build")
        with WorkingDir(buildDir):
            RunCommand(
             ["sed", "-i",
              "s"
              "#    include/libclipboard-config.h"
              "#    ${CMAKE_BINARY_DIR}/include/libclipboard-config.h"
              "#g",
              "../CMakeLists.txt"],
             verbose)
            RunCommand(
             [
              "cmake", "..",
              "-DCMAKE_TOOLCHAIN_FILE=" + configCmake.GetCrossFileName(),
              "-DCMAKE_INSTALL_PREFIX=" + installPrefix,
              "-DCMAKE_C_FLAGS=-std=c99 -Wall -pedantic -g -I./include "
              "-I../include -D_POSIX_C_SOURCE=199309L",
              "-DCMAKE_VERBOSE_MAKEFILE:BOOL=ON", "-DCMAKE_AR=" + ar
             ],
             verbose)
            RunCommand(["make"], verbose)
            RunCommand(["make", "install"], verbose)
    except CommandError:
        print("VGAZER: Unable to install", software)
        raise InstallError(software + " not installed")

    print("VGAZER:", software, "installed")

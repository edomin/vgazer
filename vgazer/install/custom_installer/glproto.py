import os

from vgazer.command         import GetCommandOutputUtf8
from vgazer.command         import RunCommand
from vgazer.exceptions      import CommandError
from vgazer.exceptions      import GithubApiRateLimitExceeded
from vgazer.exceptions      import InstallError
from vgazer.github_common   import GithubCheckApiRateLimitExceeded
from vgazer.platform        import GetInstallPrefix
from vgazer.platform        import GetTriplet
from vgazer.store.temp      import StoreTemp
from vgazer.working_dir     import WorkingDir

def Install(auth, software, platform, platformData, mirrors, verbose):
    installPrefix = GetInstallPrefix(platformData)
    targetTriplet = GetTriplet(platformData["target"])

    storeTemp = StoreTemp()
    storeTemp.ResolveEmptySubdirectory(software)
    tempPath = storeTemp.GetSubdirectoryPath(software)

    tags = auth["github"].GetJson(
     "https://api.github.com/repos/freedesktop/glproto/tags")

    if GithubCheckApiRateLimitExceeded(tags):
        raise GithubApiRateLimitExceeded(
         "Github API rate limit reached while searching last version of "
         "repo: freedesktop/glproto"
        )

    tagNum = 0
    for tag in tags:
        if tag["name"] in [
         "xo-6_7_0",
         "xf86-012804-2330",
         "xf86-4_4_99_1",
         "xf86-4_4_0",
         "xf86-4_3_99_903",
         "xf86-4_3_99_903_special",
         "xf86-4_3_99_902",
         "xf86-4_3_99_901",
         "xf86-4_3_99_16",
         "xf86-4_3_0_1",
         "sco_port_update-base",
         "rel-0-6-1",
         "lg3d-rel-0-7-0",
         "lg3d-rel-0-6-2",
         "lg3d-base",
        ]:
            tagNum = tagNum + 1
        else:
            break

    tarballUrl = tags[tagNum]["tarball_url"]
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
             ["./autogen.sh", "--host=" + targetTriplet,
              "--prefix=" + installPrefix],
             verbose)
            RunCommand(["make"], verbose)
            RunCommand(["make", "install"], verbose)
    except CommandError:
        print("VGAZER: Unable to install", software)
        raise InstallError(software + " not installed")

    print("VGAZER:", software, "installed")

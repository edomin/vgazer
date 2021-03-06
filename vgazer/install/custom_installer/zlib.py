import os
import requests
from bs4 import BeautifulSoup

from vgazer.command     import RunCommand
from vgazer.env_vars    import SetEnvVar
from vgazer.exceptions  import CommandError
from vgazer.exceptions  import InstallError
from vgazer.platform    import GetInstallPrefix
from vgazer.platform    import GetTriplet
from vgazer.store.temp  import StoreTemp
from vgazer.working_dir import WorkingDir

def GetTarballUrl():
    response = requests.get("http://zlib.net/")
    html = response.content.decode("utf-8")
    parsedHtml = BeautifulSoup(html, "html.parser")

    links = parsedHtml.find_all("a")
    for link in links:
        if link["href"].startswith("zlib") and link["href"].endswith("tar.gz"):
            return "http://zlib.net/" + link["href"]

def Install(auth, software, platform, platformData, mirrors, verbose):
    installPrefix = GetInstallPrefix(platformData)
    targetTriplet = GetTriplet(platformData["target"])
    targetOs = platformData["target"].GetOs()

    storeTemp = StoreTemp()
    storeTemp.ResolveEmptySubdirectory(software)
    tempPath = storeTemp.GetSubdirectoryPath(software)

    tarballUrl = GetTarballUrl()
    tarballShortFilename = tarballUrl.split("/")[-1]

    try:
        with WorkingDir(tempPath):
            RunCommand(["wget", "-P", "./", tarballUrl], verbose)
            RunCommand(
             ["tar", "--verbose", "--extract", "--gzip", "--file",
              tarballShortFilename],
             verbose)
        SetEnvVar("CHOST", targetTriplet)
        extractedDir = os.path.join(tempPath, tarballShortFilename[0:-7])
        with WorkingDir(extractedDir):
            if targetOs == "windows":
                RunCommand(
                 ["make", "-f", "./win32/Makefile.gcc",
                  "PREFIX=" + targetTriplet + "-"],
                 verbose)
                if not os.path.exists(installPrefix + "/include"):
                    RunCommand(["mkdir", "-p", installPrefix + "/include"],
                     verbose)
                if not os.path.exists(installPrefix + "/lib"):
                    RunCommand(["mkdir", "-p", installPrefix + "/lib"],
                     verbose)
                RunCommand(
                 ["make", "install", "-f", "./win32/Makefile.gcc",
                  "prefix=" + installPrefix,
                  "BINARY_PATH=" + installPrefix + "/bin",
                  "INCLUDE_PATH=" + installPrefix + "/include",
                  "LIBRARY_PATH=" + installPrefix + "/lib"],
                 verbose)
            else:
                RunCommand(
                 ["./configure", "--prefix=" + installPrefix], verbose)
                RunCommand(["make"], verbose)
                RunCommand(["make", "install"], verbose)
    except CommandError:
        print("VGAZER: Unable to install", software)
        raise InstallError(software + " not installed")

    print("VGAZER:", software, "installed")

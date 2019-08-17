import os
import requests
from bs4 import BeautifulSoup

from vgazer.command         import RunCommand
from vgazer.exceptions      import CommandError
from vgazer.exceptions      import InstallError
from vgazer.exceptions      import TarballLost
from vgazer.platform        import GetInstallPrefix
from vgazer.store.temp      import StoreTemp
from vgazer.working_dir     import WorkingDir

def GetTarballUrl():
    response = requests.get("http://www.portaudio.com/download.html")
    html = response.content.decode("utf-8")
    parsedHtml = BeautifulSoup(html, "html.parser")

    links = parsedHtml.find_all("a")

    for link in links:
        if link["href"].find("archives/pa_stable_") != -1:
            strongs = link.findChildren("strong")
            if len(strongs) == 1:
                return "http://www.portaudio.com/" + link["href"]

    raise TarballLost(
     "Unable to find tarball with last stable release of portaudio")

def Install(auth, software, platform, platformData, verbose):
    installPrefix = GetInstallPrefix(platformData)

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
        extractedDir = os.path.join(tempPath, "portaudio")
        with WorkingDir(extractedDir):
            RunCommand(["./configure"], verbose)
            RunCommand(["make"], verbose)
            RunCommand(["make", "install"], verbose)
    except CommandError:
        print("Unable to install", software)
        raise InstallError(software + " not installed")

    print(software, "installed")

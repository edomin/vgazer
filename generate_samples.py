#!/usr/bin/env python3

import os
import stat

from libvgazer          import Vgazer
from libvgazer.platform import GetTriplet
from libvgazer.platform import Platform

anyPlatform = Platform(arch="any", os="any", osVersion="any", abi="any")

def AddHostInstallEntries(gazer, installList, hostPlatformsList, software,
 projects):
    for hostPlatform in hostPlatformsList:
        if gazer.ChooseProject(projects, hostPlatform) is not None:
            installList.append([software, hostPlatform, anyPlatform])

def AddTargetInstallEntries(gazer, installList, hostPlatformsList,
 targetPlatformsList, software, projects):
    for hostPlatform in hostPlatformsList:
        for targetPlatform in targetPlatformsList:
            if gazer.ChooseProject(projects, targetPlatform) is not None:
                installList.append([software, hostPlatform, targetPlatform])
        targetPlatform = hostPlatform
        if gazer.ChooseProject(projects, targetPlatform) is not None:
            installList.append([software, hostPlatform, targetPlatform])

def CreateInstallList(gazer, hostPlatformsList, targetPlatformsList):
    installList = []
    softwareData = gazer.GetSoftwareData().GetData().items()
    for software, data in sorted(softwareData):
        if data["platform"] == "host":
            AddHostInstallEntries(gazer, installList, hostPlatformsList,
             software, data["projects"])
        else:
            AddTargetInstallEntries(gazer, installList, hostPlatformsList,
             targetPlatformsList, software, data["projects"])
    return installList

def GenerateImageLaunchTarget(hostPlatform):
    return ("image_{1}_{2}_{3}_launch:\n"
     "\tdocker run --net=host --entrypoint {0} -i -t \\\n"
     "     -v ~/.vgazer:/root/.vgazer -v `pwd`:/mnt/vgazer \\\n"
     "     --entrypoint sh vgazer_min_env_{1}_{2}_{3} \\\n"
     "\n".format("/bin/bash", hostPlatform.GetArch(), hostPlatform.GetOs(),
      hostPlatform.GetOsVersion()))

def GenerateSoftwareVersionsTarget(hostPlatform, targetPlatform):
    if targetPlatform.PlatformsEqual(hostPlatform):
        targetPlatformString = "host"
    else:
        targetPlatformString = "{0}_{1}_{2}".format(targetPlatform.GetArch(),
         targetPlatform.GetOs(), targetPlatform.GetAbi())
    return ("sample_{0}_{1}_{2}_software_versions_{3}:\n"
     "\tdocker run --net=host -i -t \\\n"
     "     -v ~/.vgazer:/root/.vgazer \\\n"
     "     -v `pwd`:/mnt/vgazer --entrypoint sh vgazer_min_env_{0}_{1}_{2} \\\n"
     "     -E -c ./samples/software_versions_{3}.py | tee versions.log\n"
     "\n".format(hostPlatform.GetArch(), hostPlatform.GetOs(),
      hostPlatform.GetOsVersion(), targetPlatformString))

def GenerateInstallAndVersionTarget(installEntry):
    software = installEntry[0]
    hostPlatform = installEntry[1]
    targetPlatform = installEntry[2]

    if targetPlatform.PlatformsEqual(hostPlatform):
        targetTriplet = GetTriplet(targetPlatform)
        targetInstallString = software
        targetArg = ""
    elif targetPlatform == anyPlatform:
        targetTriplet = "any-any-any"
        targetInstallString = software
        targetArg = ""
    else:
        targetTriplet = GetTriplet(targetPlatform)
        targetInstallString = "{0}-{1}".format(software, targetTriplet)
        targetArg = "--target={triplet}".format(triplet=targetTriplet)
    return (
     "sample-{harch}-{hos}-{hver}-version-{platform}:\n"
     "\tdocker run --net=host -i -t \\\n"
     "     -v ~/.vgazer:/root/.vgazer \\\n"
     "     -v `pwd`:/mnt/vgazer -v `pwd`/.vgazer-{triplet}:/mnt/vgazer_output \\\n"
     "     --entrypoint ./vgazer vgazer_min_env_{harch}_{hos}_{hver} \\\n"
     "     version {targetArg} {software} | tee version.log\n"
     "\n"
     "sample-{harch}-{hos}-{hver}-install-{platform}:\n"
     "\tdocker run --net=host -i -t \\\n"
     "     -v ~/.vgazer:/root/.vgazer \\\n"
     "     -v `pwd`:/mnt/vgazer -v `pwd`/.vgazer-{triplet}:/mnt/vgazer_output \\\n"
     "     --entrypoint ./vgazer vgazer_min_env_{harch}_{hos}_{hver} \\\n"
     "     install {targetArg} {software} | tee install.log\n"
     "\n".format(
        harch=hostPlatform.GetArch(),
        hos=hostPlatform.GetOs(),
        hver=hostPlatform.GetOsVersion(),
        platform=targetInstallString,
        software=software,
        triplet=targetTriplet,
        targetArg=targetArg
    ))

def GenerateSampleTargets(gazer, hostPlatformsList, targetPlatformsList,
 installList):
    with open("./sample_targets.mk", "w") as sampleTargetsFile:
        for hostPlatform in hostPlatformsList:
            imageLaunchTarget = GenerateImageLaunchTarget(hostPlatform)
            sampleTargetsFile.write(imageLaunchTarget)
            targetPlatform = hostPlatform
        for installEntry in installList:
            installTarget = GenerateInstallAndVersionTarget(installEntry)
            sampleTargetsFile.write(installTarget)

def main():
    gazer = Vgazer(supportOnly=True)
    hostPlatformsList = [
        Platform(arch=gazer.GetHostPlatform().GetArch(), os="debian",
         osVersion="stretch", abi="gnu", suppressGenericFallback=True),
        Platform(arch=gazer.GetHostPlatform().GetArch(), os="debian",
         osVersion="buster", abi="gnu", suppressGenericFallback=True),
        Platform(arch=gazer.GetHostPlatform().GetArch(), os="debian",
         osVersion="bullseye", abi="gnu", suppressGenericFallback=True),
        Platform(arch=gazer.GetHostPlatform().GetArch(), os="debian",
         osVersion="bookworm", abi="gnu", suppressGenericFallback=True),
        Platform(arch=gazer.GetHostPlatform().GetArch(), os="steamrt",
         osVersion="latest", abi="gnu", suppressGenericFallback=True),
    ]
    targetPlatformsList = [
        Platform(arch="x86_64", os="linux", osVersion="any", abi="gnu"),
        Platform(arch="x86_64", os="windows", osVersion="any", abi="mingw32"),
    ]
    installList = CreateInstallList(gazer, hostPlatformsList,
     targetPlatformsList)
    GenerateSampleTargets(gazer, hostPlatformsList, targetPlatformsList,
     installList)

if __name__ == "__main__":
    main()

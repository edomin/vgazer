#!/usr/bin/env python3

import os
import sys
import inspect

currentFrame = inspect.currentframe()
currentFile = os.path.abspath(inspect.getfile(currentFrame))
currentDir = os.path.dirname(currentFile)
parentDir = os.path.dirname(currentDir)

sys.path.insert(0, parentDir)

from vgazer.vgazer import Vgazer

def main():
    gazer = Vgazer()

    print("host:", gazer.GetHostPlatform().GetArch(),
     gazer.GetHostPlatform().GetOs(), gazer.GetHostPlatform().GetOsVersion(),
     gazer.GetHostPlatform().GetAbi())
    print("target:", gazer.GetTargetPlatform().GetArch(),
     gazer.GetTargetPlatform().GetOs(),
     gazer.GetTargetPlatform().GetOsVersion(),
     gazer.GetTargetPlatform().GetAbi())

    if gazer.GetHostPlatform().GetOs() == "alpine":
        gazer.Install(gazer.GetHostPlatform().GetArch() + "-linux-musl-gcc",
         verbose=True)
        gazer.Install("make", verbose=True)
        gazer.Install("autoconf", verbose=True)
        gazer.Install("automake", verbose=True)
        gazer.Install("libtool", verbose=True)
        gazer.Install("file", verbose=True)
        gazer.Install("musl", verbose=True)
        gazer.Install("sdl2", verbose=True)
    gazer.Install("sdl2_gfx", verbose=True)

if __name__ == "__main__":
    main()
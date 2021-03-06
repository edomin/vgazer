from vgazer.platform    import GetCc
from vgazer.platform    import GetCxx
from vgazer.platform    import GetInstallPrefix
from vgazer.platform    import GetTriplet
from vgazer.platform    import Platform
from vgazer.store.temp  import StoreTemp

class ConfigCmake():
    def __init__(self, platformData):
        self.storeTemp = StoreTemp(".vgazer/cmake")
        self.crossFileName = self.storeTemp.GetDirectoryFilePath(
         "toolchain.cmake")
        self.storeTemp.ResolveDirectory()
        self.platformData = platformData

    def GetCrossFileName(self):
        return self.crossFileName

    def GenerateCrossFile(self):
        print("VGAZER: Generating CMake toolchain file...")
        cmakeOs = Platform.GetGenericOs(
          self.platformData["target"].GetOs()
         ).capitalize()
        prefix = GetInstallPrefix(self.platformData)
        targetTriplet = GetTriplet(self.platformData["target"])

        cc = GetCc(self.platformData["target"])
        cxx = GetCxx(self.platformData["target"])

        if self.platformData["target"].PlatformsEqual(
         self.platformData["host"]):
            findMode = "BOTH"
        else:
            findMode = "ONLY"

        self.storeTemp.DirectoryWriteTextFile("toolchain.cmake",
         "set(CMAKE_SYSTEM_NAME {cmakeOs})\n"
         "set(CMAKE_SYSTEM_PROCESSOR {cpu})\n"
         "set(CMAKE_C_COMPILER {cc})\n"
         "set(CMAKE_CXX_COMPILER {cxx})\n"
         "set(CMAKE_FIND_ROOT_PATH {prefix})\n"
         "SET("
          "ENV{{PKG_CONFIG_LIBDIR}} "
          "${{CMAKE_FIND_ROOT_PATH}}/lib/pkgconfig/:"
          "/usr/lib/{triplet}/pkgconfig"
         ")\n"
         "SET(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)\n"
         "SET(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY {findMode})\n"
         "SET(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE {findMode})".format(
          cmakeOs=cmakeOs,
          cpu=self.platformData["target"].GetArch(),
          cc=cc,
          cxx=cxx,
          prefix=prefix,
          triplet=targetTriplet,
          findMode=findMode
         )
        )

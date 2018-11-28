import os
import platform
import tempfile

from cpt.packager import ConanMultiPackager

from conans import tools


def macos_builds():
    b1 = ({}, {}, {}, {})  # Use default compiler
    return {"https://github.com/conan-community/conan-zlib.git": [b1],
            "https://github.com/conan-community/conan-bzip2.git": [b1]}


def linux_builds():
    b1 = ({"compiler": "gcc",
           "compiler.version": "7",
           "build_type": "Release",
           "arch": "x86_64"}, {}, {}, {})
    return {"https://github.com/conan-community/conan-zlib.git": [b1],
            "https://github.com/conan-community/conan-bzip2.git": [b1]}


def windows_builds():
    b1 = ({"compiler": "Visual Studio",
           "compiler.version": "14",
           "compiler.runtime": "MD",
           "build_type": "Release",
           "arch": "x86_64"}, {}, {}, {})
    b2 = ({"compiler": "Visual Studio",
           "compiler.version": "15",
           "compiler.runtime": "MD",
           "build_type": "Release",
           "arch": "x86_64"}, {}, {}, {})
    return {"https://github.com/conan-community/conan-zlib.git": [b1, b2]}

def process():
    folder = tempfile.mkdtemp(suffix='c3i')
    with tools.environment_append({"CONAN_USER_HOME": folder,
                                   "CONAN_USERNAME": "conan",
                                   "CONAN_USE_DOCKER": "1",
                                   "CONAN_DOCKER_USE_SUDO": "0"}):
        if platform.system() == "Linux":
            confs = linux_builds()
        elif platform.system() == "Darwin":
            confs = macos_builds()
        elif platform.system() == "Windows":
            confs = windows_builds()
        else:
            raise Exception("Unknown platform: %s" % platform.system())

        for url_repo, builds in confs.items():
            pname = url_repo.split("/")[-1].replace(".git", "")
            os.system("git clone %s %s" % (url_repo, pname))
            with tools.chdir(pname):
                builder = ConanMultiPackager()
                builder.builds = builds
                builder.run()


if __name__ == "__main__":
    process()

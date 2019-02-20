import os
import platform
import tempfile


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
    
    # Check virtualenv
    if platform.system() == "Linux":
        ret = os.system("virtualenv --help")
        if ret != 0:
            raise Exception("virtualenv is needed in Linux")
    
    folder = tempfile.mkdtemp(suffix='c3i')
    env = {"CONAN_USER_HOME": folder,
           "CONAN_USERNAME": "conan"}

    with tools.environment_append(env):
        confs = {"Linux": linux_builds(),
                 "Darwin": macos_builds(),
                 "Windows": windows_builds()}.get(platform.system(), None)
        if confs is None:
            raise Exception("Unknown platform: %s" % platform.system())

        for url_repo, builds in confs.items():
            pname = url_repo.split("/")[-1].replace(".git", "")
            os.system("git clone %s %s" % (url_repo, pname))
            with tools.chdir(pname):
                os.system("conan create . user/channel")


if __name__ == "__main__":
    process()

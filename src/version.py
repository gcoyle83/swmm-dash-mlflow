import sys


def python_version():
    version_string = sys.version.split(" ")[0].split(".")
    major = version_string[0]
    minor = version_string[1]
    patch = version_string[2]

    return (major, minor, patch)

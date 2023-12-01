from src.version import python_version


def test_python_version():
    major, minor, _ = python_version()
    assert (major, minor) == (str(3), str(12))

import re
from importlib.metadata import version


def test_package_is_installed() -> None:
    assert re.fullmatch(r"\d+\.\d+\.\d+", version("asofar")) is not None

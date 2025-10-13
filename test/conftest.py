from collections import namedtuple
import os
from pathlib import Path
import sys

from container_ci_suite.utils import check_variables

if not check_variables():
    sys.exit(1)

Vars = namedtuple("Vars", ["OS", "VERSION", "IMAGE_NAME", "IS_MINIMAL", "VERSION_NO_FCGID", "SHORT_VERSION", "TEST_DIR"])
VERSION = os.getenv("VERSION")
VARS = Vars(
    OS=os.getenv("TARGET").lower(),
    VERSION=VERSION,
    IMAGE_NAME=os.getenv("IMAGE_NAME"),
    IS_MINIMAL="minimal" in VERSION,
    VERSION_NO_FCGID=VERSION.replace("-mod_fcgid", ""),
    SHORT_VERSION=VERSION.replace("-mod_fcgid", "").replace(".", ""),
    TEST_DIR=Path(__file__).parent.absolute()
)

TAGS = {
    "rhel8": "-ubi8",
    "rhel9": "-ubi9",
    "rhel10": "-ubi10",
}

MYSQL_TAGS = {
    "rhel8": "-el8",
    "rhel9": "-el9",
    "rhel10": "-el10",
}

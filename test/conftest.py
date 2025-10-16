import os
import sys

from pathlib import Path
from collections import namedtuple
from pytest import skip

from container_ci_suite.utils import check_variables

if not check_variables():
    sys.exit(1)

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

Vars = namedtuple(
    "Vars", [
        "OS", "TAG", "MYSQL_VERSION", "VERSION", "IMAGE_NAME", "IS_MINIMAL",
        "VERSION_NO_FCGID", "SHORT_VERSION", "TEST_DIR"
    ]
)
VERSION = os.getenv("VERSION")
OS = os.getenv("TARGET").lower()
VARS = Vars(
    OS=OS,
    TAG=TAGS.get(OS),
    MYSQL_VERSION=f"8.0{MYSQL_TAGS.get(OS)}",
    VERSION=VERSION,
    IMAGE_NAME=os.getenv("IMAGE_NAME"),
    IS_MINIMAL="minimal" in VERSION,
    VERSION_NO_FCGID=VERSION.replace("-mod_fcgid", ""),
    SHORT_VERSION=VERSION.replace("-mod_fcgid", "").replace(".", ""),
    TEST_DIR=Path(__file__).parent.absolute()
)

IMAGE_TAG = f"mysql:{VARS.MYSQL_VERSION}"


def skip_helm_charts_tests():
    if VARS.VERSION == "5.32" and VARS.OS == "rhel8":
        skip(f"Skipping Helm Charts tests for {VARS.VERSION} on {VARS.OS}.")

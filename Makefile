# Variables are documented in hack/build.sh.
BASE_IMAGE_NAME = perl
# 5.24 disabled because CentOS is missing rh-perl524 repository
VERSIONS = 5.16 5.20
OPENSHIFT_NAMESPACES = 5.16

# Include common Makefile code.
include hack/common.mk

# Variables are documented in common/build.sh.
BASE_IMAGE_NAME = perl
VERSIONS = 5.26-mod_fcgid 5.26 5.30 5.32 5.34 5.36 5.38 5.40
OPENSHIFT_NAMESPACES = 5.16

# HACK:  Ensure that 'git pull' for old clones doesn't cause confusion.
# New clones should use '--recursive'.
.PHONY: $(shell test -f common/common.mk || echo >&2 'Please do "git submodule update --init" first.')

include common/common.mk

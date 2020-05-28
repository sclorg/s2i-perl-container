#!/bin/bash
#
# Functions for tests for the Perl image in OpenShift.
#
# IMAGE_NAME specifies a name of the candidate image used for testing.
# The image has to be available before this script is executed.
#

THISDIR=$(dirname ${BASH_SOURCE[0]})

source "${THISDIR}/test-lib.sh"
source "${THISDIR}/test-lib-openshift.sh"

# Check the imagestream
function test_perl_imagestream() {
  case ${OS} in
    rhel7|centos7) ;;
    *) echo "Imagestream testing not supported for $OS environment." ; return 0 ;;
  esac
  
  ct_os_test_image_stream_quickstart "${THISDIR}/imagestreams/perl-${OS}.json" \
                                     "${THISDIR}/sample-test-app.json" \
                                     "${IMAGE_NAME}" \
                                     perl \
                                     "Everything is OK" \
                                     8080 http 200 "-p SOURCE_REPOSITORY_REF=staging -p VERSION=${VERSION} -p NAME=perl-testing"
}

# vim: set tabstop=2:shiftwidth=2:expandtab:


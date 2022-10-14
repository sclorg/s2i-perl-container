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
    rhel7|centos7|rhel8|rhel9) ;;
    *) echo "Imagestream testing not supported for $OS environment." ; return 0 ;;
  esac

  local tag="-el7"
  if [ "${OS}" == "rhel8" ]; then
    tag="-el8"
  elif [ "${OS}" == "rhel9" ]; then
    tag="-el9"
  fi
  echo "Testing perl imagestream application"
  ct_os_test_image_stream_quickstart "${THISDIR}/imagestreams/perl-${OS%[0-9]*}.json" \
                                     "${THISDIR}/sample-test-app.json" \
                                     "${IMAGE_NAME}" \
                                     perl \
                                     "Everything is OK" \
                                     8080 http 200 "-p SOURCE_REPOSITORY_REF=staging -p VERSION=${VERSION}${tag} -p NAME=perl-testing"
}

function test_perl_s2i_sample_app() {
  # TODO: We should ideally use a local directory instead of ${VERSION}/test/sample-test-app,
  # so we can test changes in that example app that are done as part of the PR
  ct_os_test_s2i_app ${IMAGE_NAME} "https://github.com/sclorg/s2i-perl-container.git" "${VERSION}/test/sample-test-app" "Everything is OK"
}

function test_perl_s2i_dancer_app() {
  ct_os_test_s2i_app ${IMAGE_NAME} "https://github.com/sclorg/dancer-ex.git" . 'Welcome to your Dancer application on OpenShift'
}

function test_perl_s2i_templates() {
  # TODO: this was not working because the referenced example dir was added as part of this commit
  ct_os_test_template_app "${IMAGE_NAME}" \
                        "https://raw.githubusercontent.com/sclorg/s2i-perl-container/master/examples/templates/sample-test-app.json" \
                        perl \
                        "Everything is OK" \
                        8080 http 200 \
                        "-p SOURCE_REPOSITORY_REF=staging -p VERSION=${VERSION} -p NAME=perl-testing"
}
# vim: set tabstop=2:shiftwidth=2:expandtab:


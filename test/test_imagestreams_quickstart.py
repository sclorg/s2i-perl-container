import os
import sys

import pytest

from container_ci_suite.openshift import OpenShiftAPI
from container_ci_suite.utils import check_variables


if not check_variables():
    print("At least one variable from IMAGE_NAME, OS, VERSION is missing.")
    sys.exit(1)


VERSION = os.getenv("VERSION")
IMAGE_NAME = os.getenv("IMAGE_NAME")
OS = os.getenv("OS")

TAGS = {
    "rhel8": "-ubi8",
    "rhel9": "-ubi9",
    "rhel10": "-ubi10"
}

TAG = TAGS.get(OS, None)

if VERSION == "5.30-mod_fcgid":
    VERSION = "5.30"

if VERSION == "5.26-mod_fcgid":
    VERSION = "5.26"


# Replacement with 'test_python_s2i_templates'
class TestImagestreamsQuickstart:

    def setup_method(self):
        self.oc_api = OpenShiftAPI(pod_name_prefix="perl-testing", version=VERSION)

    def teardown_method(self):
        self.oc_api.delete_project()

    def test_perl_template_inside_cluster(self):
        if OS == "rhel10":
            pytest.skip("Do NOT test on RHEL10 yet.")
        service_name = "perl-testing"
        assert self.oc_api.imagestream_quickstart(
            imagestream_file="imagestreams/perl-rhel.json",
            template_file="examples/templates/sample-test-app.json",
            image_name=IMAGE_NAME,
            name_in_template="perl",
            openshift_args=[
                f"SOURCE_REPOSITORY_REF=master",
                f"VERSION={VERSION}{TAG}",
                f"NAME={service_name}"
            ]
        )
        assert self.oc_api.is_template_deployed(name_in_template=service_name, timeout=480)
        assert self.oc_api.check_response_inside_cluster(
            name_in_template=service_name, expected_output="Everything is OK"
        )

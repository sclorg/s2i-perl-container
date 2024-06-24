import os
import sys

import pytest

from container_ci_suite.openshift import OpenShiftAPI
from container_ci_suite.utils import check_variables


if not check_variables():
    print("At least one variable from IMAGE_NAME, OS, SINGLE_VERSION is missing.")
    sys.exit(1)


VERSION = os.getenv("SINGLE_VERSION")
IMAGE_NAME = os.getenv("IMAGE_NAME")
OS = os.getenv("OS")

TAGS = {
    "rhel7": "-ubi7",
    "rhel8": "-ubi8",
    "rhel9": "-ubi9"
}

TAG = TAGS.get(OS, None)


# Replacement with 'test_python_s2i_templates'
class TestImagestreamsQuickstart:

    def setup_method(self):
        self.oc_api = OpenShiftAPI(pod_name_prefix="perl-testing", version=VERSION)

    def teardown_method(self):
        self.oc_api.delete_project()

    def test_perl_template_inside_cluster(self):
        new_version = VERSION
        if VERSION == "5.26-mod_fcgid":
            new_version = "5.26"
        service_name = "perl-testing"
        assert self.oc_api.imagestream_quickstart(
            imagestream_file="imagestreams/perl-rhel.json",
            template_file="examples/templates/sample-test-app.json",
            image_name=IMAGE_NAME,
            name_in_template="perl",
            openshift_args=[
                f"SOURCE_REPOSITORY_REF=master",
                f"VERSION={new_version}{TAG}",
                f"NAME={service_name}"
            ]
        )
        assert self.oc_api.template_deployed(name_in_template=service_name)
        assert self.oc_api.check_response_inside_cluster(
            name_in_template=service_name, expected_output="Everything is OK"
        )

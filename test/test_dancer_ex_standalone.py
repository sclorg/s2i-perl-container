import os
import sys

import pytest

from container_ci_suite.utils import check_variables
from container_ci_suite.openshift import OpenShiftAPI

if not check_variables():
    print("At least one variable from IMAGE_NAME, OS, VERSION is missing.")
    sys.exit(1)


VERSION = os.getenv("VERSION")
IMAGE_NAME = os.getenv("IMAGE_NAME")
OS = os.getenv("TARGET")


# Replacement with 'test_python_s2i_app_ex'
class TestPerlDancerExTemplate:

    def setup_method(self):
        self.oc_api = OpenShiftAPI(pod_name_prefix="perl-testing", version=VERSION, shared_cluster=True)

    def teardown_method(self):
        self.oc_api.delete_project()

    def test_dancer_ex_template_inside_cluster(self):
        service_name = "perl-testing"
        assert self.oc_api.deploy_s2i_app(
            image_name=IMAGE_NAME, app="https://github.com/sclorg/dancer-ex.git",
            context=".",
            service_name=service_name
        )
        assert self.oc_api.template_deployed(name_in_template=service_name, timeout=480)
        assert self.oc_api.check_response_inside_cluster(
            name_in_template=service_name, expected_output="Welcome to your Dancer application on OpenShift"
        )

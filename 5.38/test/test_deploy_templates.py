import os
import sys

from container_ci_suite.openshift import OpenShiftAPI
from container_ci_suite.utils import check_variables

if not check_variables():
    print("At least one variable from IMAGE_NAME, OS, VERSION is missing.")
    sys.exit(1)


VERSION = os.getenv("VERSION")
IMAGE_NAME = os.getenv("IMAGE_NAME")
OS = os.getenv("TARGET")


class TestDeployTemplate:

    def setup_method(self):
        self.oc_api = OpenShiftAPI(pod_name_prefix="perl-testing", version=VERSION)
        self.oc_api.import_is("imagestreams/perl-rhel.json", "", skip_check=True)

    def teardown_method(self):
        self.oc_api.delete_project()

    def test_perl_template_inside_cluster(self):
        service_name = "perl-testing"
        assert self.oc_api.deploy_template_with_image(
            image_name=IMAGE_NAME,
            template=f"examples/templates/sample-test-app.json",
            name_in_template="perl",
            openshift_args=[
                f"SOURCE_REPOSITORY_REF=master",
                f"VERSION={VERSION}",
                f"NAME={service_name}"
            ]
        )
        assert self.oc_api.template_deployed(name_in_template=service_name)
        assert self.oc_api.check_response_inside_cluster(
            name_in_template=service_name, expected_output="Everything is OK"
        )

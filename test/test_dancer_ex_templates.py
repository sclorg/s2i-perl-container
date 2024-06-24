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
OS = os.getenv("TARGET")

DEPLOYED_MYSQL_IMAGE = "quay.io/sclorg/mysql-80-c9s:c9s"

MYSQL_TAGS = {
    "rhel8": "-el8",
    "rhel9": "-el9"
}
MYSQL_TAG = MYSQL_TAGS.get(OS, None)
IMAGE_TAG = f"mysql:8.0{MYSQL_TAG}"
MYSQL_VERSION = f"8.0{MYSQL_TAG}"


class TestDeployDancerExTemplateWithoutMySQL:

    def setup_method(self):
        self.oc_api = OpenShiftAPI(pod_name_prefix="perl-testing", version=VERSION)
        self.oc_api.import_is("imagestreams/perl-rhel.json", "", skip_check=True)

    def teardown_method(self):
        self.oc_api.delete_project()

    def test_perl_template_inside_cluster(self):
        service_name = "perl-testing"
        template_url = self.oc_api.get_raw_url_for_json(
            container="dancer-ex", dir="openshift/templates", filename="dancer.json", branch="master"
        )
        assert self.oc_api.deploy_template_with_image(
            image_name=IMAGE_NAME,
            template=template_url,
            name_in_template="perl",
            openshift_args=[
                f"SOURCE_REPOSITORY_REF=master",
                f"PERL_VERSION={VERSION}",
                f"NAME={service_name}",
                "SOURCE_REPOSITORY_REF=master"
            ]
        )
        assert self.oc_api.template_deployed(name_in_template=service_name)
        assert self.oc_api.check_response_inside_cluster(
            name_in_template=service_name, expected_output="Welcome to your Dancer application on OpenShift"
        )


class TestDeployDancerExTemplateWithMySQL:

    def setup_method(self):
        self.oc_api = OpenShiftAPI(pod_name_prefix="perl-testing", version=VERSION)
        self.oc_api.import_is("imagestreams/perl-rhel.json", "", skip_check=True)
        assert self.oc_api.upload_image(DEPLOYED_MYSQL_IMAGE, f"{IMAGE_TAG}")

    def teardown_method(self):
        self.oc_api.delete_project()

    def test_perl_template_inside_cluster(self):
        service_name = "perl-testing"
        template_url = self.oc_api.get_raw_url_for_json(
            container="dancer-ex", dir="openshift/templates", filename="dancer-mysql-persistent.json", branch="master"
        )
        assert self.oc_api.deploy_template_with_image(
            image_name=IMAGE_NAME,
            template=template_url,
            name_in_template="perl",
            openshift_args=[
                f"SOURCE_REPOSITORY_REF=master",
                f"PERL_VERSION={VERSION}",
                f"NAME={service_name}",
                f"MYSQL_VERSION={MYSQL_VERSION}"

            ]
        )
        assert self.oc_api.template_deployed(name_in_template=service_name)
        assert self.oc_api.check_response_inside_cluster(
            name_in_template=service_name, expected_output="Welcome to your Dancer application on OpenShift"
        )

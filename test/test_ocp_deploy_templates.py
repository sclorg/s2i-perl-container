from container_ci_suite.openshift import OpenShiftAPI

from conftest import VARS


class TestDeployTemplate:

    def setup_method(self):
        self.oc_api = OpenShiftAPI(
            pod_name_prefix=f"perl-{VARS.SHORT_VERSION}-testing",
            version=VARS.SHORT_VERSION,
            shared_cluster=True
        )

    def teardown_method(self):
        self.oc_api.delete_project()

    def test_perl_template_inside_cluster(self):
        self.oc_api.import_is("imagestreams/perl-rhel.json", "", skip_check=True)
        service_name = f"perl-{VARS.SHORT_VERSION}-testing"
        assert self.oc_api.deploy_template_with_image(
            image_name=VARS.IMAGE_NAME,
            template="examples/templates/sample-test-app.json",
            name_in_template="perl",
            openshift_args=[
                "SOURCE_REPOSITORY_REF=master",
                f"VERSION={VARS.SHORT_VERSION}",
                f"NAME={service_name}"
            ]
        )
        assert self.oc_api.is_template_deployed(name_in_template=service_name, timeout=480)
        assert self.oc_api.check_response_inside_cluster(
            name_in_template=service_name, expected_output="Everything is OK"
        )

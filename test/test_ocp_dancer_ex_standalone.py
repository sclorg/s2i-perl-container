from container_ci_suite.openshift import OpenShiftAPI

from conftest import VARS


class TestPerlDancerExTemplate:

    def setup_method(self):
        self.oc_api = OpenShiftAPI(
            pod_name_prefix=f"perl-{VARS.SHORT_VERSION}-testing",
            version=VARS.VERSION,
            shared_cluster=True
        )

    def teardown_method(self):
        self.oc_api.delete_project()

    def test_dancer_ex_template_inside_cluster(self):
        """
        Test checks if example GitHub application dancer-ex
        works properly and response is as expected
        """
        service_name = f"perl-{VARS.SHORT_VERSION}-testing"
        assert self.oc_api.deploy_s2i_app(
            image_name=VARS.IMAGE_NAME, app="https://github.com/sclorg/dancer-ex.git",
            context=".",
            service_name=service_name
        )
        assert self.oc_api.is_s2i_pod_running(pod_name_prefix=service_name, cycle_count=480)
        assert self.oc_api.check_response_inside_cluster(
            name_in_template=service_name, expected_output="Welcome to your Dancer application on OpenShift"
        )

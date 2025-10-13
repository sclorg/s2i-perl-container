from container_ci_suite.openshift import OpenShiftAPI


from conftest import VARS, TAGS, skip_helm_charts_tests


# Replacement with 'test_python_s2i_templates'
class TestImagestreamsQuickstart:

    def setup_method(self):
        self.oc_api = OpenShiftAPI(
            pod_name_prefix=f"perl-{VARS.SHORT_VERSION}-testing",
            version=VARS.SHORT_VERSION,
            shared_cluster=True
        )

    def teardown_method(self):
        self.oc_api.delete_project()

    def test_perl_template_inside_cluster(self):
        skip_helm_charts_tests()
        service_name = f"perl-{VARS.SHORT_VERSION}-testing"
        assert self.oc_api.imagestream_quickstart(
            imagestream_file="imagestreams/perl-rhel.json",
            template_file="examples/templates/sample-test-app.json",
            image_name=VARS.IMAGE_NAME,
            name_in_template="perl",
            openshift_args=[
                "SOURCE_REPOSITORY_REF=master",
                f"VERSION={VARS.VERSION_NO_FCGID}{TAGS.get(VARS.OS)}",
                f"NAME={service_name}"
            ]
        )
        assert self.oc_api.is_template_deployed(name_in_template=service_name, timeout=480)
        assert self.oc_api.check_response_inside_cluster(
            name_in_template=service_name, expected_output="Everything is OK"
        )

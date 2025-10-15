from container_ci_suite.openshift import OpenShiftAPI

from conftest import VARS, MYSQL_VERSION, IMAGE_TAG

DEPLOYED_MYSQL_IMAGE = "quay.io/sclorg/mysql-80-c9s:c9s"


class TestDeployDancerExTemplateWithoutMySQL:

    def setup_method(self):
        self.oc_api = OpenShiftAPI(
            pod_name_prefix=f"perl-{VARS.SHORT_VERSION}-testing", version=VARS.SHORT_VERSION, shared_cluster=True
        )

    def teardown_method(self):
        self.oc_api.delete_project()

    def test_perl_template_inside_cluster(self):
        """
        Test checks if local imagestream and GitHub application dancer-ex
        works properly and response is as expected.
        The response is taken from POD `command-app`
        executed inside the same project.
        """
        self.oc_api.import_is("imagestreams/perl-rhel.json", "", skip_check=True)
        service_name = f"perl-{VARS.SHORT_VERSION}-testing"
        template_url = self.oc_api.get_raw_url_for_json(
            container="dancer-ex", dir="openshift/templates", filename="dancer.json", branch="master"
        )
        assert self.oc_api.deploy_template_with_image(
            image_name=VARS.IMAGE_NAME,
            template=template_url,
            name_in_template="perl",
            openshift_args=[
                f"PERL_VERSION={VARS.SHORT_VERSION}",
                f"NAME={service_name}",
                "SOURCE_REPOSITORY_REF=master"
            ]
        )
        assert self.oc_api.is_template_deployed(name_in_template=service_name, timeout=480)
        assert self.oc_api.check_response_inside_cluster(
            name_in_template=service_name, expected_output="Welcome to your Dancer application on OpenShift"
        )


class TestDeployDancerExTemplateWithMySQL:

    def setup_method(self):

        self.oc_api = OpenShiftAPI(
            pod_name_prefix=f"perl-{VARS.SHORT_VERSION}-testing", version=VARS.SHORT_VERSION
        )

    def teardown_method(self):
        self.oc_api.delete_project()

    def test_perl_template_inside_cluster(self):
        """
        Test checks if local imagestream and GitHub application dancer-ex
        works properly and response is as expected.
        MySQL persistent database is enabled as well.
        The response is taken from POD `command-app`
        executed inside the same project.
        """
        self.oc_api.import_is("imagestreams/perl-rhel.json", "", skip_check=True)
        assert self.oc_api.upload_image(DEPLOYED_MYSQL_IMAGE, f"{IMAGE_TAG}")
        service_name = f"perl-{VARS.SHORT_VERSION}-testing"
        template_url = self.oc_api.get_raw_url_for_json(
            container="dancer-ex",
            dir="openshift/templates",
            filename="dancer-mysql-persistent.json",
            branch="master"
        )
        assert self.oc_api.deploy_template_with_image(
            image_name=VARS.IMAGE_NAME,
            template=template_url,
            name_in_template="perl",
            openshift_args=[
                "SOURCE_REPOSITORY_REF=master",
                f"PERL_VERSION={VARS.SHORT_VERSION}",
                f"NAME={service_name}",
                f"MYSQL_VERSION={MYSQL_VERSION}"

            ]
        )
        assert self.oc_api.is_template_deployed(name_in_template=service_name, timeout=480)
        assert self.oc_api.check_response_inside_cluster(
            name_in_template=service_name, expected_output="Welcome to your Dancer application on OpenShift"
        )

from container_ci_suite.helm import HelmChartsAPI

from conftest import VARS, TAGS


class TestHelmPerlDancerAppTemplate:

    def setup_method(self):
        package_name = "redhat-perl-dancer-application"
        self.hc_api = HelmChartsAPI(
            path=VARS.TEST_DIR,
            package_name=package_name,
            tarball_dir=VARS.TEST_DIR,
            shared_cluster=True
        )
        self.hc_api.clone_helm_chart_repo(
            repo_url="https://github.com/sclorg/helm-charts", repo_name="helm-charts",
            subdir="charts/redhat"
        )

    def teardown_method(self):
        self.hc_api.delete_project()

    def test_dancer_application_helm_test(self):
        self.hc_api.package_name = "redhat-perl-imagestreams"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        self.hc_api.package_name = "redhat-perl-dancer-application"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation(
            values={
                "perl_version": f"{VARS.VERSION_NO_FCGID}{TAGS.get(VARS.OS)}",
                "namespace": self.hc_api.namespace
            }
        )
        assert self.hc_api.is_s2i_pod_running(pod_name_prefix="dancer-example", timeout=400)
        assert self.hc_api.test_helm_chart(expected_str=["Welcome to your Dancer application"])

import pytest

from container_ci_suite.helm import HelmChartsAPI

from conftest import VARS


class TestHelmRHELPerlImageStreams:

    def setup_method(self):
        package_name = "redhat-perl-imagestreams"
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

    @pytest.mark.parametrize(
        "version,registry,expected",
        [
            ("5.40-ubi10", "registry.redhat.io/ubi10/perl-540:latest", True),
            ("5.32-ubi9", "registry.redhat.io/ubi9/perl-532:latest", True),
            ("5.32-ubi8", "registry.redhat.io/ubi8/perl-532:latest", False),
            ("5.26-ubi8", "registry.redhat.io/ubi8/perl-526:latest", True),
        ],
    )
    def test_package_imagestream(self, version, registry, expected):
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        assert self.hc_api.check_imagestreams(version=version, registry=registry) == expected

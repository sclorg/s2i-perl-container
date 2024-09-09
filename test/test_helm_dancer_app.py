import os
import sys

import pytest

from pathlib import Path

from container_ci_suite.helm import HelmChartsAPI
from container_ci_suite.utils import check_variables

if not check_variables():
    print("At least one variable from IMAGE_NAME, OS, VERSION is missing.")
    sys.exit(1)

test_dir = Path(os.path.abspath(os.path.dirname(__file__)))


class TestHelmPerlDancerAppTemplate:

    def setup_method(self):
        package_name = "perl-dancer-application"
        path = test_dir
        self.hc_api = HelmChartsAPI(path=path, package_name=package_name, tarball_dir=test_dir, remote=True)
        self.hc_api.clone_helm_chart_repo(
            repo_url="https://github.com/sclorg/helm-charts", repo_name="helm-charts",
            subdir="charts/redhat"
        )

    def teardown_method(self):
        self.hc_api.delete_project()

    def test_dancer_application_curl_output(self):
        if self.hc_api.oc_api.shared_cluster:
            pytest.skip("Do NOT test on shared cluster")
        self.hc_api.package_name = "perl-imagestreams"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        self.hc_api.package_name = "perl-dancer-application"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation(
            values={
                "perl_version": "5.32-ubi8",
                "namespace": self.hc_api.namespace
            }
        )
        assert self.hc_api.is_s2i_pod_running(pod_name_prefix="dancer-example")
        assert self.hc_api.test_helm_curl_output(
            route_name="dancer-example",
            expected_str="Welcome to your Dancer application"
        )

    def test_dancer_application_helm_test(self):
        self.hc_api.package_name = "perl-imagestreams"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        self.hc_api.package_name = "perl-dancer-application"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation(
            values={
                "perl_version": "5.32-ubi8",
                "namespace": self.hc_api.namespace
            }
        )
        assert self.hc_api.is_s2i_pod_running(pod_name_prefix="dancer-example")
        assert self.hc_api.test_helm_chart(expected_str=["Welcome to your Dancer application"])

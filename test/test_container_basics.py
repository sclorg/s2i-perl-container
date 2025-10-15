import pytest

from container_ci_suite.container_lib import ContainerTestLib
from container_ci_suite.engines.podman_wrapper import PodmanCLIWrapper

from conftest import VARS


class TestPerlContainer:

    def setup_method(self):
        self.app = ContainerTestLib(image_name=VARS.IMAGE_NAME, s2i_image=True)

    def teardown_method(self):
        self.app.cleanup()

    def test_run_s2i_usage(self):
        """
        Test checks if `usage` script works properly
        """
        output = self.app.s2i_usage()
        assert output

    # # test_docker_run_usage
    def test_docker_run_usage(self):
        """
        Test checks if `docker run` script works properly and do not fail
        """
        assert PodmanCLIWrapper.call_podman_command(
            cmd=f"run --rm {VARS.IMAGE_NAME} &>/dev/null",
            return_output=False
        ) == 0

    def test_scl_usage(self):
        """
        Test checks if command `perl --version` script works properly
        and returns version without -mod_fcgid
        """
        assert f"v{VARS.VERSION_NO_FCGID}" in PodmanCLIWrapper.podman_run_command(
            f"--rm {VARS.IMAGE_NAME} /bin/bash -c 'perl --version'"
        )

    @pytest.mark.parametrize(
        "dockerfile",
        [
            "Dockerfile",
            "Dockerfile.s2i"
        ]
    )
    def test_dockerfiles(self, dockerfile):
        """
        Test checks if we are able to build a container from
        `examples/from-dockerfile/<version>/{Dockerfile,Dockerfile.s2i}
        """
        assert self.app.build_test_container(
            dockerfile=VARS.TEST_DIR / "examples/from-dockerfile" / VARS.VERSION / dockerfile,
            app_url="https://github.com/sclorg/dancer-ex.git",
            app_dir="app-src"
        )
        assert self.app.test_app_dockerfile()
        cip = self.app.get_cip()
        assert cip
        assert self.app.test_response(
            url=cip, expected_code=200,
            expected_output="Welcome to your Dancer application"
        )

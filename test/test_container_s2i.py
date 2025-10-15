import re
from time import sleep

import pytest

from pathlib import Path

from container_ci_suite.container_lib import ContainerTestLib
from container_ci_suite.engines.podman_wrapper import PodmanCLIWrapper
from container_ci_suite.engines.container import ContainerImage

from conftest import VARS

sample_test_app = VARS.TEST_DIR / "sample-test-app"
bin_app = VARS.TEST_DIR / "binpath"
fcgi = VARS.TEST_DIR / "fcgi"
psgi = VARS.TEST_DIR / "psgi"
psgi_hot_deploy = VARS.TEST_DIR / "psgi-hot_deploy"
psgi_variables = VARS.TEST_DIR / "psgi-variables"
warningonstderr = VARS.TEST_DIR / "warningonstderr"


def build_npm_app(app_path: Path) -> ContainerTestLib:
    container_lib = ContainerTestLib(VARS.IMAGE_NAME)
    s2i_app = container_lib.build_as_df(
        app_path=app_path,
        s2i_args=f"--pull-policy=never {container_lib.build_s2i_npm_variables()}",
        src_image=VARS.IMAGE_NAME,
        dst_image=f"{VARS.IMAGE_NAME}-testapp"
    )
    return s2i_app


def build_s2i_app(app_path: Path, container_args: str = "") -> ContainerTestLib:
    container_lib = ContainerTestLib(VARS.IMAGE_NAME)
    app_name = app_path.name
    s2i_app = container_lib.build_as_df(
        app_path=app_path,
        s2i_args=f"--pull-policy=never {container_args} {container_lib.build_s2i_npm_variables()}",
        src_image=VARS.IMAGE_NAME,
        dst_image=f"{VARS.IMAGE_NAME}-{app_name}"
    )
    return s2i_app


class TestPerlSampleTestAppContainer:
    def setup_method(self):
        self.s2i_app = build_s2i_app(sample_test_app)

    def teardown_method(self):
        self.s2i_app.cleanup()

    def test_run_s2i_usage(self):
        """
        Test checks if `usage` script works properly
        """
        output = self.s2i_app.s2i_usage()
        assert output

    # test_docker_run_usage
    def test_docker_run_usage(self):
        """
        Test checks if `docker run` script works properly and do not fail
        """
        assert PodmanCLIWrapper.call_podman_command(
            cmd=f"run --rm {VARS.IMAGE_NAME} &>/dev/null",
            return_output=False
        ) == 0

    @pytest.mark.parametrize(
        "container_arg",
        [
            "",
            "-u 12345"
        ]
    )
    def test_run_app_test(self, container_arg):
        """
        Test checks if we are able to run a container as deamon
        and response works as expected
        """
        cid_file_name = self.s2i_app.app_name
        assert self.s2i_app.create_container(cid_file_name=cid_file_name, container_args=container_arg)
        assert ContainerImage.wait_for_cid(cid_file_name=cid_file_name)
        cid = self.s2i_app.get_cid(cid_file_name=cid_file_name)
        assert cid
        cip = self.s2i_app.get_cip(cid_file_name=cid_file_name)
        assert cip
        assert self.s2i_app.test_response(
            url=f"http://{cip}", expected_code=200
        )


@pytest.mark.parametrize(
    "application_path,container_args,page,expected_output",
    [
        (bin_app, "", "/", "Usage"),
        (psgi, "", "/", "<title>Web::Paste::Simple"),
        (psgi_variables, "--env=PSGI_FILE=./application2.psgi --env=PSGI_URI_PATH=/path",
            "/path", "<title>Web::Paste::Simple"),
        (psgi_variables, "--env=PSGI_FILE=./application2.psgi --env=PSGI_URI_PATH=/path",
            "/cpanfile", "requires"),
        (warningonstderr, "", "/", "Text in HTTP body"),
        (fcgi, "", "/", "Index FCGI script"),
        (fcgi, "", "/another.fcgi", "Another FCGI script"),
    ]
)
class TestPerlExampleAppContainer:
    def test_run_app_test(self, application_path, container_args, page, expected_output):
        """
        Test class checks specific applications
        and response works as expected. See parametrized parameters for more
        details
        """
        self.s2i_app = build_s2i_app(application_path, container_args=container_args)
        cid_file_name = self.s2i_app.app_name
        assert self.s2i_app.create_container(
            cid_file_name=cid_file_name, container_args=f"--user=100001 {container_args}"
        )
        assert ContainerImage.wait_for_cid(cid_file_name=cid_file_name)
        cid = self.s2i_app.get_cid(cid_file_name=cid_file_name)
        assert cid
        cip = self.s2i_app.get_cip(cid_file_name=cid_file_name)
        assert cip
        if application_path == warningonstderr:
            assert self.s2i_app.test_response(
                url=f"http://{cip}", expected_code=200, expected_output=expected_output, page=page, debug=True
            )
            output_logs = self.s2i_app.get_logs(cid_file_name=cid_file_name)
            assert re.search('GET / HTTP/1.1\" 200', output_logs)
            assert re.search("Warning on stderr", output_logs)
        else:
            assert self.s2i_app.test_response(
                url=f"http://{cip}", expected_code=200, expected_output=expected_output, page=page, debug=True
            )


class TestPerlNPMtestContainer:
    def setup_method(self):
        self.s2i_app = build_npm_app(sample_test_app)

    def teardown_method(self):
        self.s2i_app.cleanup()

    def test_npm_works(self):
        """
        Test checks if NPM works in container.
        """
        assert self.s2i_app.npm_works(image_name=VARS.IMAGE_NAME)


@pytest.mark.parametrize(
    "application_path,container_args,hot_deploy",
    [
        (psgi_hot_deploy, "--env=PSGI_FILE=./index.psgi", False),
        (psgi_hot_deploy, "--env=PSGI_FILE=./index.psgi --env=PSGI_RELOAD=1", True),
    ]
)
class TestPerlHotDeployAppContainer:
    def test_run_app_test(self, application_path, container_args, hot_deploy):
        """
        Test checks hot deploy application
        It checks what is present in HTTP response
        """
        self.s2i_app = build_s2i_app(application_path, container_args=container_args)
        cid_file_name = self.s2i_app.app_name
        assert self.s2i_app.create_container(
            cid_file_name=cid_file_name, container_args=f"--user=100001 {container_args}"
        )
        assert ContainerImage.wait_for_cid(cid_file_name=cid_file_name)
        cid = self.s2i_app.get_cid(cid_file_name=cid_file_name)
        assert cid
        cip = self.s2i_app.get_cip(cid_file_name=cid_file_name)
        assert cip
        assert self.s2i_app.test_response(
            url=f"http://{cip}", expected_output="old initial value: 0"
        )
        assert self.s2i_app.test_response(
            url=f"http://{cip}", expected_output="old initial value: 1"
        )
        # We need to wait couple seconds till container
        # before changing 'string' in 'Test.pm' file
        # If we don't set PSGI_RELOAD, this change don't affects application.
        # If we set PSGI_RELOAD, this change affects application.
        sleep(3)
        PodmanCLIWrapper.podman_exec_shell_command(
            cid_file_name=cid,
            cmd="sed -ie 's/old initial value/new initial value/' lib/My/Test.pm",
            used_shell="/bin/sh"
        )
        if hot_deploy:
            # We need to wait couple seconds till container
            # does not update page. HotDeploy needs at least 3 seconds
            sleep(3)
            assert PodmanCLIWrapper.podman_exec_shell_command(
                cid_file_name=cid,
                cmd="grep 'new initial' lib/My/Test.pm",
                used_shell="/bin/sh"
            )
            assert self.s2i_app.test_response(
                url=f"http://{cip}", expected_output="new initial value: 0"
            )
        else:
            assert self.s2i_app.test_response(
                url=f"http://{cip}", expected_output="old initial value: 2"
            )

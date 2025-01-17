Perl container images
=====================

[![Build and push images to Quay.io registry](https://github.com/sclorg/s2i-perl-container/actions/workflows/build-and-push.yml/badge.svg)](https://github.com/sclorg/s2i-perl-container/actions/workflows/build-and-push.yml)

Images available on Quay are:
* CentOS Stream 9 [perl-5.32](https://quay.io/repository/sclorg/perl-532-c9s)
* CentOS Stream 10 [perl-5.40](https://quay.io/repository/sclorg/perl-540-c10s)
* Fedora [perl-5.32](https://quay.io/repository/fedora/perl-532)
* Fedora [perl-5.34](https://quay.io/repository/fedora/perl-534)
* Fedora [perl-5.36](https://quay.io/repository/fedora/perl-536)
* Fedora [perl-5.38](https://quay.io/repository/fedora/perl-538)
* Fedora [perl-5.40](https://quay.io/repository/fedora/perl-540)

This repository contains the source for building various versions of
the Perl application as a reproducible container image using
[source-to-image](https://github.com/openshift/source-to-image).
Users can choose between RHEL and CentOS based builder images.
The resulting image can be run using [podman](https://github.com/containers/libpod).

For more information about using these images with OpenShift, please see the
official [OpenShift Origin documentation](https://docs.okd.io/latest/using_images/s2i_images/perl.html).

For more information about contributing, see
[the Contribution Guidelines](https://github.com/sclorg/welcome/blob/master/contribution.md).
For more information about concepts used in these container images, see the
[Landing page](https://github.com/sclorg/welcome).


Versions
--------
Perl versions currently provided:
* [perl-5.26](5.26)
* [perl-5.30](5.30)
* [perl-5.32](5.32)
* [perl-5.34](5.34)
* [perl-5.36](5.36)
* [perl-5.38](5.38)
* [perl-5.40](5.40)

RHEL versions currently supported:
* RHEL8
* RHEL9
* RHEL10

CentOS versions currently supported:
* CentOS Stream 9
* CentOS Stream 10


Installation
------------
To build a Perl image, choose either the CentOS Stream or RHEL based image:

*  **RHEL based image**

    These images are available in the [Red Hat Container Catalog](https://access.redhat.com/containers/#/registry.access.redhat.com/rhel8/perl-532).
    To download it run:

    ```
    $ podman pull registry.access.redhat.com/rhel8/perl-532
    ```

    To build a RHEL based Perl image, you need to run the build on a properly
    subscribed RHEL machine.

    ```
    $ git clone --recursive https://github.com/sclorg/s2i-perl-container.git
    $ cd s2i-perl-container
    $ make build TARGET=rhel8 VERSIONS=5.32
    ```

*  **CentOS Stream based image**

    This image is available on DockerHub. To download the perl-5.32 image, run:

    ```
    $ podman pull quay.io/sclorg/perl-532
    ```

    To build the perl-5.32 image from scratch run:

    ```
    $ git clone --recursive https://github.com/sclorg/s2i-perl-container.git
    $ cd s2i-perl-container
    $ make build TARGET=c9s VERSIONS=5.32
    ```

Note: while the installation steps are calling `podman`, you can replace any such calls by `docker` with the same arguments.

**Notice: By omitting the `VERSIONS` parameter, the build/test action will be performed
on all provided versions of Perl.**


Usage
-----

For information about usage of the Dockerfile for Perl 5.30,
see [usage documentation](5.30/README.md).

For information about usage of the Dockerfile for Perl 5.32 - mod_fcgid version,
see [usage documentation](5.32/README.md).

For information about usage of the Dockerfile for Perl 5.34 - mod_fcgid version,
see [usage documentation](5.34/README.md).

For information about usage of the Dockerfile for Perl 5.36 - mod_fcgid version,
see [usage documentation](5.36/README.md).

For information about usage of the Dockerfile for Perl 5.38 - mod_fcgid version,
see [usage documentation](5.38/README.md).

For information about usage of the Dockerfile for Perl 5.40 - mod_fcgid version,
see [usage documentation](5.40/README.md).

Test
----
This repository also provides a [S2I](https://github.com/openshift/source-to-image) test framework,
which launches tests to check functionality of a simple Perl application built on top of the s2i-perl image.

Users can choose between testing a Perl test application based on a RHEL or CentOS image.

*  **RHEL based image**

    To test a RHEL8-based image, you need to run the test on a properly
    subscribed RHEL machine.

    ```
    $ cd s2i-perl-container
    $ make test TARGET=rhel8 VERSIONS=5.32
    ```

*  **CentOS Stream based image**

    ```
    $ cd s2i-perl-container
    $ make test TARGET=c9s VERSIONS=5.32
    ```

**Notice: By omitting the `VERSIONS` parameter, the build/test action will be performed
on all of the provided versions of Perl.**


Repository organization
-----------------------
* **`<perl-version>`**

    * **Dockerfile.c9s**

        CentOS Stream based Dockerfile.

    * **Dockerfile.c10s**

        CentOS Stream based Dockerfile.

    * **Dockerfile.rhel8**

        RHEL based Dockerfile. In order to perform build or test actions on this
        Dockerfile you need to run the action on a properly subscribed RHEL machine.

    * **`s2i/bin/`**

        This folder contains scripts that are run by [S2I](https://github.com/openshift/source-to-image):

        *   **assemble**

            Used to install the sources into a location where the application
            will be run and prepare the application for deployment (eg. installing
            modules, etc.).
            In order to install application dependencies, the application must contain a
            `cpanfile` file, in which the user specifies the modules and their versions.
            An example of a [cpanfile](https://github.com/sclorg/s2i-perl-container/blob/master/5.30/test/sample-test-app/cpanfile) is available within our test application.

            All files with `.cgi` and `.pl` extension are handled by mod_perl.
            If exactly one file with `.psgi` extension exists in the top-level
            directory, the mod_perl will be autoconfigured to execute the PSGI
            application for any request URI path with Plack's mod_perl adaptor.

        *   **run**

            This script is responsible for running the application, using the
            Apache web server.

        *   **usage***

            This script prints the usage of this image.

    * **`contrib/`**

        This folder contains a file with commonly used modules.

    * **`test/`**

        This folder contains the [S2I](https://github.com/openshift/source-to-image)
        test framework.

        * **`sample-test-app/`**

            A simple Perl application used for testing purposes by the [S2I](https://github.com/openshift/source-to-image) test framework.

        * **run**

            This script runs the [S2I](https://github.com/openshift/source-to-image) test framework.

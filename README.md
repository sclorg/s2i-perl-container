Perl Docker images
==================

This repository contains the source for building various versions of
the Perl application as a reproducible Docker image using
[source-to-image](https://github.com/openshift/source-to-image).
Users can choose between RHEL and CentOS based builder images.
The resulting image can be run using [Docker](http://docker.io).

For more information about using these images with OpenShift, please see the
official [OpenShift Origin documentation](https://docs.openshift.org/latest/using_images/s2i_images/perl.html).

For more information about contributing, see
[the Contribution Guidelines](https://github.com/sclorg/welcome/blob/master/contribution.md).
For more information about concepts used in these docker images, see the
[Landing page](https://github.com/sclorg/welcome).


Versions
---------------
Perl versions currently provided:
* perl-5.16 (deprecated)
* [perl-5.20](5.20)
* [perl-5.24](5.24)

RHEL versions currently supported:
* RHEL7

CentOS versions currently supported:
* CentOS7


Installation
---------------
To build a Perl image, choose either the CentOS or RHEL based image:

*  **RHEL based image**

    To build a RHEL based Perl image, you need to run the build on a properly
    subscribed RHEL machine.

    ```
    $ git clone --recursive https://github.com/sclorg/s2i-perl-container.git
    $ cd s2i-perl-container
    $ make build TARGET=rhel7 VERSIONS=5.24
    ```

*  **CentOS based image**

    This image is available on DockerHub. To download the perl-5.24 image, run:

    ```
    $ docker pull centos/perl-524-centos7
    ```

    To build the perl-5.24 image from scratch run:

    ```
    $ git clone --recursive https://github.com/sclorg/s2i-perl-container.git
    $ cd s2i-perl-container
    $ make build TARGET=centos7 VERSIONS=5.24
    ```

**Notice: By omitting the `VERSIONS` parameter, the build/test action will be performed
on all provided versions of Perl.**


Usage
---------------------------------

For information about usage of the Dockerfile for Perl 5.16,
see [usage documentation](5.16/README.md)

For information about usage of the Dockerfile for Perl 5.20,
see [usage documentation](5.20/README.md).

For information about usage of the Dockerfile for Perl 5.24,
see [usage documentation](5.24/README.md).


Test
---------------------
This repository also provides a [S2I](https://github.com/openshift/source-to-image) test framework,
which launches tests to check functionality of a simple Perl application built on top of the s2i-perl image.

Users can choose between testing a Perl test application based on a RHEL or CentOS image.

*  **RHEL based image**

    To test a RHEL7-based image, you need to run the test on a properly
    subscribed RHEL machine.

    ```
    $ cd s2i-perl-container
    $ make test TARGET=rhel7 VERSIONS=5.24
    ```

*  **CentOS based image**

    ```
    $ cd s2i-perl-container
    $ make test TARGET=centos7 VERSIONS=5.24
    ```

**Notice: By omitting the `VERSIONS` parameter, the build/test action will be performed
on all of the provided versions of Perl.**



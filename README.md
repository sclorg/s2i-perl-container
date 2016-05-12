Perl Docker images
==================

This repository contains the source for building various versions of
the Perl application as a reproducible Docker image using
[source-to-image](https://github.com/openshift/source-to-image).
Users can choose between RHEL and CentOS based builder images.
The resulting image can be run using [Docker](http://docker.io).

For more information about using these images with OpenShift, please see the
official [OpenShift Documentation](https://docs.openshift.org/latest/using_images/s2i_images/perl.html).

Versions
---------------
Perl versions currently provided are:
* perl-5.16
* perl-5.20

RHEL versions currently supported are:
* RHEL7

CentOS versions currently supported are:
* CentOS7


Installation
---------------
To build a Perl image, choose either the CentOS or RHEL based image:
*  **RHEL based image**

    To build a RHEL based perl-5.16 image, you need to run the build on a properly
    subscribed RHEL machine.

    ```
    $ git clone https://github.com/openshift/s2i-perl.git
    $ cd s2i-perl
    $ make build TARGET=rhel7 VERSION=5.16
    ```

*  **CentOS based image**

    This image is available on DockerHub. To download perl-5.16 image, run:

    ```
    $ docker pull openshift/perl-516-centos7
    ```

    To build the perl-5.16 image from scratch run:

    ```
    $ git clone https://github.com/openshift/s2i-perl.git
    $ cd s2i-perl
    $ make build VERSION=5.16
    ```

**Notice: By omitting the `VERSION` parameter, the build/test action will be performed
on all provided versions of Perl.**


Usage
---------------------------------

For information about usage of Dockerfile for Perl 5.16,
see [usage documentation](5.16/README.md).

For information about usage of Dockerfile for Perl 5.20,
see [usage documentation](5.20/README.md).


Test
---------------------
This repository also provides a [S2I](https://github.com/openshift/source-to-image) test framework,
which launches tests to check functionality of a simple Perl application built on top of the s2i-perl image.

Users can choose between testing a Perl test application based on a RHEL or CentOS image.

*  **RHEL based image**

    To test a RHEL7-based image, you need to run the test on a properly
    subscribed RHEL machine.

    ```
    $ cd s2i-perl
    $ make test TARGET=rhel7 VERSION=5.16
    ```

*  **CentOS based image**

    ```
    $ cd s2i-perl
    $ make test VERSION=5.16
    ```

**Notice: By omitting the `VERSION` parameter, the build/test action will be performed
on all the provided versions of Perl.**


Repository organization
------------------------
* **`<perl-version>`**

    Dockerfile and scripts to build container images from.

* **`hack/`**

    Folder containing scripts which are responsible for the build and test actions performed by the `Makefile`.


Image name structure
------------------------
##### Structure: openshift/1-2-3

1. Platform name (lowercase) - perl
2. Platform version(without dots) - 516
3. Base builder image - centos7/rhel7

Examples: `openshift/perl-516-centos7`, `openshift/perl-516-rhel7`


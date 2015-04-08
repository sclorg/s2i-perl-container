Perl for OpenShift - Docker images
========================================

This repository contains sources of the images for building various versions
of Perl applications as reproducible Docker images using
[source-to-image](https://github.com/openshift/source-to-image).
User can choose between RHEL and CentOS based builder images.
The resulting image can be run using [Docker](http://docker.io).


Versions
---------------
Perl versions currently provided are:
* perl-5.16

RHEL versions currently supported are:
* RHEL7

CentOS versions currently supported are:
* CentOS7


Installation
---------------
To build Perl image, choose between CentOS or RHEL based image:
*  **RHEL based image**

    To build a rhel-based perl-5.16 image, you need to run the build on a properly
    subscribed RHEL machine.

    ```
    $ git clone https://github.com/openshift/sti-perl.git
    $ cd sti-perl
    $ make build TARGET=rhel7 VERSION=5.16
    ```

*  **CentOS based image**

    This image is available on DockerHub. To download it use:

    ```
    $ docker pull openshift/perl-516-centos7
    ```

    To build Perl image from scratch use:

    ```
    $ git clone https://github.com/openshift/sti-perl.git
    $ cd sti-perl
    $ make build VERSION=5.16
    ```

**Notice: By omitting the `VERSION` parameter, the build/test action will be performed
on all provided versions of Perl. Since we are now providing only version `5.16`,
you can omit this parameter.**


Usage
---------------------
To build a simple [perl-sample-app](https://github.com/openshift/sti-perl/tree/master/5.16/test/sample-test-app) application,
using standalone [STI](https://github.com/openshift/source-to-image) and then run the
resulting image with [Docker](http://docker.io) execute:

*  **For RHEL based image**
    ```
    $ sti build https://github.com/openshift/sti-perl.git --contextDir=5.16/test/sample-test-app/ openshift/perl-516-rhel7 perl-sample-app
    $ docker run -p 8080:8080 perl-sample-app
    ```

*  **For CentOS based image**
    ```
    $ sti build https://github.com/openshift/sti-perl.git --contextDir=5.16/test/sample-test-app/ openshift/perl-516-centos7 perl-sample-app
    $ docker run -p 8080:8080 perl-sample-app
    ```

**Accessing the application:**
```
$ curl 127.0.0.1:8080
```


Test
---------------------
This repository also provides [STI](https://github.com/openshift/source-to-image) test framework,
which launches tests to check functionality of a simple perl application built on top of sti-perl image.

User can choose between testing perl test application based on RHEL or CentOS image.

*  **RHEL based image**

    To test a rhel7-based perl-5.16 image, you need to run the test on a properly
    subscribed RHEL machine.

    ```
    $ cd sti-perl
    $ make test TARGET=rhel7 VERSION=5.16
    ```

*  **CentOS based image**

    ```
    $ cd sti-perl
    $ make test VERSION=5.16
    ```

**Notice: By omitting the `VERSION` parameter, the build/test action will be performed
on all the provided versions of Perl. Since we are now providing only version `5.16`
you can omit this parameter.**


Repository organization
------------------------
* **`<perl-version>`**

    * **Dockerfile**

        CentOS based Dockerfile.

    * **Dockerfile.rhel7**

        RHEL based Dockerfile. In order to perform build or test actions on this
        Dockerfile you need to run the action on a properly subscribed RHEL machine.

    * **`.sti/bin/`**

        This folder contains scripts that are run by [STI](https://github.com/openshift/source-to-image):

        *   **assemble**

            Is used to install the sources into location from where the application
            will be run and prepare the application for deployment (eg. installing
            modules, etc.).
            In order to install application dependencies, application has to contain 
            `cpanfile`, in which user specifies modules and their versions.
            Example of [cpanfile](https://github.com/openshift/sti-perl/blob/master/5.16/test/sample-test-app/cpanfile) is available in our test application.  

        *   **run**

            This script is responsible for running the application, by using the
            apache web server.

        *   **usage***

            This script prints the usage of this image.

    * **`contrib/`**

        This folder contains file with commonly used modules.

    * **`test/`**

        This folder is containing [STI](https://github.com/openshift/source-to-image)
        test framework.

        * **`sample-test-app/`**

            Simple Perl application used for testing purposes in the [STI](https://github.com/openshift/source-to-image) test framework.

        * **run**

            Script that runs the [STI](https://github.com/openshift/source-to-image) test framework.

* **`hack/`**

    Folder contains scripts which are responsible for build and test actions performed by the `Makefile`.


Image name structure
------------------------
##### Structure: openshift/1-2-3

1. Platform name - perl
2. Platform version(without dots)
3. Base builder image - centos7/rhel7

Examples: `openshift/perl-516-centos7`, `openshift/perl-516-rhel7`


Environment variables
---------------------

To set these environment variables, you can place them into `.sti/environment`
file inside your source code repository.

* **ENABLE_CPAN_TEST**

    Will install all the cpan packages and run their tests. Default value is set to 
    `false`.

* **CPAN_MIRROR**

    This variable specifies mirror URL which will used by cpanminus to install dependencies. 
    By default the URL is not specified.

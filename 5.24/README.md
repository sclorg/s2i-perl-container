Perl 5.24 Docker image
=================

This container image includes Perl 5.24 as a [S2I](https://github.com/openshift/source-to-image) base image for your Perl 5.24 applications.
Users can choose between RHEL and CentOS based builder images.
The RHEL image is available in the [Red Hat Container Catalog](https://access.redhat.com/containers/#/registry.access.redhat.com/rhscl/perl-524-rhel7)
as registry.access.redhat.com/rhscl/perl-524-rhel7.
The CentOS image is then available on [Docker Hub](https://hub.docker.com/r/centos/perl-524-centos7/)
as centos/perl-524-centos7. 
The resulting image can be run using [Docker](http://docker.io).

Description
-----------

Perl 5.24 available as docker container is a base platform for 
building and running various Perl 5.24 applications and frameworks. 
Perl is a high-level programming language with roots in C, sed, awk and shell scripting. 
Perl is good at handling processes and files, and is especially good at handling text. 
Perl's hallmarks are practicality and efficiency. While it is used to do a lot of 
different things, Perl's most common applications are system administration utilities 
and web programming.

Usage
---------------------
To build a simple [perl-sample-app](https://github.com/sclorg/s2i-perl-container/tree/master/5.24/test/sample-test-app) application,
using standalone [S2I](https://github.com/openshift/source-to-image) and then run the
resulting image with [Docker](http://docker.io) execute:

*  **For RHEL based image**
    ```
    $ s2i build https://github.com/sclorg/s2i-perl-container.git --context-dir=5.24/test/sample-test-app/ rhscl/perl-524-rhel7 perl-sample-app
    $ docker run -p 8080:8080 perl-sample-app
    ```

*  **For CentOS based image**
    ```
    $ s2i build https://github.com/sclorg/s2i-perl-container.git --context-dir=5.24/test/sample-test-app/ centos/perl-524-centos7 perl-sample-app
    $ docker run -p 8080:8080 perl-sample-app
    ```

**Accessing the application:**
```
$ curl 127.0.0.1:8080
```

Environment variables
---------------------

To set environment variables, you can place them as a key value pair into a `.sti/environment`
file inside your source code repository.

* **ENABLE_CPAN_TEST**

    Allow the installation of all specified cpan packages and the running of their tests. The default value is `false`.

* **CPAN_MIRROR**

    This variable specifies a mirror URL which will used by cpanminus to install dependencies.
    By default the URL is not specified.

* **PERL_APACHE2_RELOAD**

    Set this to "true" to enable automatic reloading of modified Perl modules.

* **HTTPD_START_SERVERS**

    The [StartServers](https://httpd.apache.org/docs/2.4/mod/mpm_common.html#startservers)
    directive sets the number of child server processes created on startup. Default is 8.

* **HTTPD_MAX_REQUEST_WORKERS**

    Number of simultaneous requests that will be handled by Apache. The default
    is 256, but it will be automatically lowered if memory is limited.

* **PSGI_FILE**

    Override PSGI application detection.

    If the PSGI_FILE variable is set to empty value, no PSGI application will
    be detected and mod_perl not be reconfigured.

    If the PSGI_FILE variable is set and non-empty, it will define path to
    the PSGI application file. No detection will be used.

    If the PSGI_FILE variable does not exist, autodetection will be used:
    If exactly one ./*.psgi file exists, mod_perl will be configured to
    execute that file.

* **PSGI_URI_PATH**

    This variable overrides location URI path that is handled path the PSGI
    application. Default value is "/".


See also
--------
Dockerfile and other sources are available on https://github.com/sclorg/s2i-perl-container.
In that repository you also can find another versions of Python environment Dockerfiles.
Dockerfile for CentOS is called Dockerfile, Dockerfile for RHEL is called Dockerfile.rhel7.

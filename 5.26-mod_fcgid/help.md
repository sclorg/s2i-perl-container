Perl 5.26 container image
=========================

This container image includes Perl 5.26 as a [S2I](https://github.com/openshift/source-to-image) base image for your Perl 5.26 applications.
Users can choose between RHEL and CentOS based builder images.
The RHEL image is available in the [Red Hat Container Catalog](https://access.redhat.com/containers/#/registry.access.redhat.com/rhel8/perl-526)
as registry.access.redhat.com/rhel8/perl-526.
The CentOS image is then available on [Docker Hub](https://hub.docker.com/r/centos/perl-526-centos8/)
as centos/perl-526-centos8. 
The resulting image can be run using [Docker](http://docker.io).

Description
-----------

Perl 5.26 available as container is a base platform for 
building and running various Perl 5.26 applications and frameworks. 
Perl is a high-level programming language with roots in C, sed, awk and shell scripting. 
Perl is good at handling processes and files, and is especially good at handling text. 
Perl's hallmarks are practicality and efficiency. While it is used to do a lot of 
different things, Perl's most common applications are system administration utilities 
and web programming.

This container image includes an npm utility, so users can use it to install JavaScript
modules for their web applications. There is no guarantee for any specific npm or nodejs
version, that is included in the image; those versions can be changed anytime and
the nodejs itself is included just to make the npm work.

Usage
---------------------
To build a simple [perl-sample-app](https://github.com/sclorg/s2i-perl-container/tree/master/5.26/test/sample-test-app) application,
using standalone [S2I](https://github.com/openshift/source-to-image) and then run the
resulting image with [Docker](http://docker.io) execute:

*  **For RHEL based image**
    ```
    $ s2i build https://github.com/sclorg/s2i-perl-container.git --context-dir=5.26/test/sample-test-app/ rhel8/perl-526 perl-sample-app
    $ docker run -p 8080:8080 perl-sample-app
    ```

*  **For CentOS based image**
    ```
    $ s2i build https://github.com/sclorg/s2i-perl-container.git --context-dir=5.26/test/sample-test-app/ centos/perl-526-centos8 perl-sample-app
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

* **HTTPD_START_SERVERS**

    The [StartServers](https://httpd.apache.org/docs/2.4/mod/mpm_common.html#startservers)
    directive sets the number of child server processes created on startup. Default is 8.

* **HTTPD_MAX_REQUEST_WORKERS**

    Number of simultaneous requests that will be handled by Apache httpd. The default
    is 256, but it will be automatically lowered if memory is limited.

* **PSGI_FILE**

    Override PSGI application detection.

    If the PSGI_FILE variable is set to an empty value, no PSGI application will
    be detected and mod_fcgid will not be reconfigured.

    If the PSGI_FILE variable is set and non-empty, it will define path to
    a PSGI application file and mod_fcgid will be configured to execute that
    file.

    If the PSGI_FILE variable does not exist, autodetection will be used:
    If exactly one ./*.psgi file exists, mod_fcgid will be configured to
    execute that file.

* **PSGI_URI_PATH**

    This variable overrides location URI path that is handled path the PSGI
    application. Default value is "/".


See also
--------
Dockerfile and other sources are available on https://github.com/sclorg/s2i-perl-container.
In that repository you also can find another versions of Perl environment Dockerfiles.
Dockerfile for CentOS is called Dockerfile, Dockerfile for RHEL is called Dockerfile.rhel8.

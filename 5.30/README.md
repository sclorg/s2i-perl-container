Perl 5.30 container image
=========================

This container image includes Perl 5.30 as an [S2I](https://github.com/openshift/source-to-image) base image for your Perl 5.30 applications.
Users can choose between RHEL, CentOS and Fedora based builder images.
The RHEL images are available in the [Red Hat Container Catalog](https://access.redhat.com/containers/),
the CentOS images are available on [Docker Hub](https://hub.docker.com/r/centos/),
and the Fedora images are available in [Fedora Registry](https://registry.fedoraproject.org/).
The resulting image can be run using [podman](https://github.com/containers/libpod).

Note: while the examples in this README are calling `podman`, you can replace any such calls by `docker` with the same arguments.

Description
-----------

Perl 5.30 available as container is a base platform for
building and running various Perl 5.30 applications and frameworks.
Perl is a high-level programming language with roots in C, sed, awk and shell scripting.
Perl is good at handling processes and files, and is especially good at handling text.
Perl's hallmarks are practicality and efficiency. While it is used to do a lot of
different things, Perl's most common applications are system administration utilities
and web programming.

This container image includes an npm utility, so users can use it to install JavaScript
modules for their web applications. There is no guarantee for any specific npm or nodejs
version, that is included in the image; those versions can be changed anytime and
the nodejs itself is included just to make the npm work.

Usage in Openshift
------------------

In this example, we will assume that you are using the `centos/perl-530-centos7` image, available via `perl:5.30` imagestream tag in Openshift.
To build a simple [nodejs-sample-app](https://github.com/sclorg/dancer-ex.git) application in Openshift:

```
oc new-app perl:5.30~https://github.com/sclorg/dancer-ex.git
```

**To access the application:**

```
oc get pods
oc exec <pod> -- curl 127.0.0.1:8080
```

Source-to-Image framework and scripts
-------------------------------------

This image supports the [Source-to-Image](https://docs.openshift.com/container-platform/3.11/creating_images/s2i.html)
(S2I) strategy in OpenShift. The Source-to-Image is an OpenShift framework
which makes it easy to write images that take application source code as
an input, use a builder image like this Perl container image, and produce
a new image that runs the assembled application as an output.

To support the Source-to-Image framework, important scripts are included in the builder image:

* The `/usr/libexec/s2i/assemble` script inside the image is run to produce a new image with the application artifacts. The script takes sources of a given application and places them into appropriate directories inside the image. It utilizes some common patterns in Perl application development (see the **Environment variables** section below).
* The `/usr/libexec/s2i/run` script is set as the default command in the resulting container image (the new image with the application artifacts). It runs `httpd` for production.

Building an application using a Dockerfile
------------------------------------------

Compared to the Source-to-Image strategy, using a Dockerfile is a more
flexible way to build a Perl container image with an application.
Use a Dockerfile when Source-to-Image is not sufficiently flexible for you or
when you build the image outside of the OpenShift environment.

To use the Perl image in a Dockerfile, follow these steps:

#### 1. Pull a base builder image to build on

```
podman pull centos/perl-530-centos7
```

An CentOs image `centos/perl-530-centos7` is used in this example.

#### 2. Pull and application code

An example application available at https://github.com/sclorg/dancer-ex.git is used here. Feel free to clone the repository for further experiments.

```
git clone https://github.com/sclorg/dancer-ex.git app-src
```

#### 3. Prepare an application inside a container

This step usually consists of at least these parts:

* putting the application source into the container
* installing the dependencies
* setting the default command in the resulting image

For all these three parts, users can either setup all manually and use commands `perl` and `cpanm` explicitly in the Dockerfile ([3.1.](#31-to-use-your-own-setup-create-a-dockerfile-with-this-content)), or users can use the Source-to-Image scripts inside the image ([3.2.](#32-to-use-the-source-to-image-scripts-and-build-an-image-using-a-dockerfile-create-a-dockerfile-with-this-content); see more about these scripts in the section "Source-to-Image framework and scripts" above), that already know how to set-up and run some common Perl applications.

##### 3.1 To use your own setup, create a Dockerfile with this content:

```
FROM centos/perl-530-centos7

# Add application sources
ADD app-src .

# Install the dependencies
RUN export PATH=${PATH}:/opt/rh/rh-perl530/root/usr/bin/&& \
     export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/opt/rh/rh-perl530/root/usr/lib64 && \
     cpanm --notest -l extlib Module::CoreList && \
     cpanm --notest -l extlib --installdeps .

CMD sed -i '1i<Location/>' /opt/app-root/etc/httpd.d/40-psgi.conf
CMD sed -i '2iSetHandler perl-script' /opt/app-root/etc/httpd.d/40-psgi.conf
CMD sed -i '3iPerlResponseHandler Plack::Handler::Apache2' /opt/app-root/etc/httpd.d/40-psgi.conf
CMD sed -i '4iPerlSetVar psgi_app app.psgi' /opt/app-root/etc/httpd.d/40-psgi.conf
CMD sed -i '5i</Location>' /opt/app-root/etc/httpd.d/40-psgi.conf

# Run scripts uses standard ways to run the application
CMD exec httpd -C 'Include /opt/app-root/etc/httpd.conf' -D FOREGROUND
```

##### 3.2 To use the Source-to-Image scripts and build an image using a Dockerfile, create a Dockerfile with this content:

```
FROM centos/perl-530-centos7

# Add application sources to a directory that the assemble scriptexpects them
# and set permissions so that the container runs without root access
USER 0
ADD app-src /tmp/src
RUN chown -R 1001:0 /tmp/src
USER 1001

# Install the dependencies
RUN /usr/libexec/s2i/assemble

# Set the default command for the resulting image
CMD /usr/libexec/s2i/run
```

#### 4. Build a new image from a Dockerfile prepared in the previous step

```
podman build -t perl-app .
```

#### 5. Run the resulting image with final application

```
podman run -d perl-app
```

Environment variables for Source-to-Image
-----------------------------------------

To set environment variables, you can place them as a key value pair into a `.s2i/environment`
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
In that repository you also can find another versions of Perl environment Dockerfiles.
Dockerfile for CentOS is called `Dockerfile`, Dockerfile for RHEL7 is called `Dockerfile.rhel7` and the Fedora Dockerfile is called `Dockerfile.fedora`.

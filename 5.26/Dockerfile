FROM centos/s2i-base-centos7

# This image provides a Perl 5.26 environment you can use to run your Perl applications.

EXPOSE 8080

# Image metadata
ENV PERL_VERSION=5.26 \
    PERL_SHORT_VER=526 \
    NAME=perl

ENV SUMMARY="Platform for building and running Perl $PERL_VERSION applications" \
    DESCRIPTION="Perl $PERL_VERSION available as container is a base platform for \
building and running various Perl $PERL_VERSION applications and frameworks. \
Perl is a high-level programming language with roots in C, sed, awk and shell scripting. \
Perl is good at handling processes and files, and is especially good at handling text. \
Perl's hallmarks are practicality and efficiency. While it is used to do a lot of \
different things, Perl's most common applications are system administration utilities \
and web programming."

LABEL summary="$SUMMARY" \
      description="$DESCRIPTION" \
      io.k8s.description="$DESCRIPTION" \
      io.k8s.display-name="Apache 2.4 with mod_perl/$PERL_VERSION" \
      io.openshift.expose-services="8080:http" \
      io.openshift.tags="builder,${NAME},${NAME}${PERL_SHORT_VER}" \
      io.openshift.s2i.scripts-url="image:///usr/libexec/s2i" \
      io.s2i.scripts-url="image:///usr/libexec/s2i" \
      name="centos/${NAME}-${PERL_SHORT_VER}-centos7" \
      com.redhat.component="rh-${NAME}${PERL_SHORT_VER}-container" \
      version="$PERL_VERSION" \
      maintainer="SoftwareCollections.org <sclorg@redhat.com>" \
      help="For more information visit https://github.com/sclorg/s2i-${NAME}-container" \
      usage="s2i build <SOURCE-REPOSITORY> centos/${NAME}-${PERL_SHORT_VER}-centos7:latest <APP-NAME>"

RUN yum install -y centos-release-scl && \
    INSTALL_PKGS="rh-perl526 rh-perl526-perl rh-perl526-perl-devel rh-perl526-mod_perl rh-perl526-perl-Apache-Reload rh-perl526-perl-CPAN rh-perl526-perl-App-cpanminus" && \
    yum install -y --setopt=tsflags=nodocs  $INSTALL_PKGS && \
    rpm -V $INSTALL_PKGS && \
    yum clean all

# Copy the S2I scripts from the specific language image to $STI_SCRIPTS_PATH
COPY ./s2i/bin/ $STI_SCRIPTS_PATH

# Copy extra files to the image.
COPY ./root/ /

# In order to drop the root user, we have to make some directories world
# writeable as OpenShift default security model is to run the container under
# random UID.
RUN mkdir -p ${APP_ROOT}/etc/httpd.d && \
    sed -i -f ${APP_ROOT}/etc/httpdconf.sed /opt/rh/httpd24/root/etc/httpd/conf/httpd.conf  && \
    chmod -R og+rwx /opt/rh/httpd24/root/var/run/httpd ${APP_ROOT}/etc/httpd.d && \
    chown -R 1001:0 ${APP_ROOT} && chmod -R ug+rwx ${APP_ROOT} && \
    rpm-file-permissions

USER 1001

# Enable the SCL for all bash scripts.
ENV BASH_ENV=${APP_ROOT}/etc/scl_enable \
    ENV=${APP_ROOT}/etc/scl_enable \
    PROMPT_COMMAND=". ${APP_ROOT}/etc/scl_enable"

# Set the default CMD to print the usage of the language image
CMD $STI_SCRIPTS_PATH/usage

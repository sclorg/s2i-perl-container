FROM quay.io/centos7/s2i-base-centos7

# This image provides a Perl 5.30 environment you can use to run your Perl applications.

EXPOSE 8080

# Image metadata
ENV PERL_VERSION=5.30 \
    PERL_SHORT_VER=530 \
    NAME=perl \
    HTTPD_24=httpd24

ENV SUMMARY="Platform for building and running Perl $PERL_VERSION applications" \
    DESCRIPTION="Perl $PERL_VERSION available as container is a base platform for \
building and running various Perl $PERL_VERSION applications and frameworks. \
Perl is a high-level programming language with roots in C, sed, awk and shell scripting. \
Perl is good at handling processes and files, and is especially good at handling text. \
Perl's hallmarks are practicality and efficiency. While it is used to do a lot of \
different things, Perl's most common applications are system administration utilities \
and web programming." \
     PKG_CONFIG_PATH=/opt/rh/$HTTPD_24/root/usr/lib64/pkgconfig \
     PYTHONPATH=/opt/rh/$NODEJS_SCL/root/usr/lib/python2.7/site-packages \
     PATH=/opt/rh/$NODEJS_SCL/root/usr/bin:/opt/app-root/src/bin:/opt/app-root/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/rh/rh-perl$PERL_SHORT_VER/root/usr/local/bin:/opt/rh/rh-perl$PERL_SHORT_VER/root/usr/bin:/opt/rh/$HTTPD_24/root/usr/bin:/opt/rh/$HTTPD_24/root/usr/sbin:/opt/app-root/src/extlib/bin \
     LD_LIBRARY_PATH=/opt/rh/$NODEJS_SCL/root/usr/lib64:/opt/rh/rh-perl$PERL_SHORT_VER/root/usr/lib64:/opt/rh/$HTTPD_24/root/usr/lib64 \
     X_SCLS="rh-perl$PERL_SHORT_VER $NODEJS_SCL $HTTPD_24" \
     LIBRARY_PATH=/opt/rh/$HTTPD_24/root/usr/lib64 \
     MANPATH=/opt/rh/$NODEJS_SCL/root/usr/share/man:/opt/rh/$HTTPD_24/root/usr/share/man:/opt/rh/rh-perl$PERL_SHORT_VER/root/usr/share/man \
     PERL5LIB=/opt/app-root/src/extlib/lib/perl5

LABEL summary="$SUMMARY" \
      description="$DESCRIPTION" \
      io.k8s.description="$DESCRIPTION" \
      io.k8s.display-name="Apache 2.4 with mod_perl/$PERL_VERSION" \
      io.openshift.expose-services="8080:http" \
      io.openshift.tags="builder,${NAME},${NAME}${PERL_SHORT_VER}" \
      io.openshift.s2i.scripts-url="image:///usr/libexec/s2i" \
      io.s2i.scripts-url="image:///usr/libexec/s2i" \
      name="centos7/${NAME}-${PERL_SHORT_VER}-centos7" \
      com.redhat.component="rh-${NAME}${PERL_SHORT_VER}-container" \
      version="$PERL_VERSION" \
      maintainer="SoftwareCollections.org <sclorg@redhat.com>" \
      help="For more information visit https://github.com/sclorg/s2i-${NAME}-container" \
      usage="s2i build <SOURCE-REPOSITORY> quay.io/centos7/${NAME}-${PERL_SHORT_VER}-centos7:latest <APP-NAME>"

RUN yum install -y centos-release-scl && \
    INSTALL_PKGS="rh-perl530 rh-perl530-perl rh-perl530-perl-devel rh-perl530-mod_perl rh-perl530-perl-Apache-Reload rh-perl530-perl-CPAN rh-perl530-perl-App-cpanminus" && \
    yum install -y --setopt=tsflags=nodocs  $INSTALL_PKGS && \
    rpm -V $INSTALL_PKGS && \
    yum -y clean all --enablerepo='*'

# Copy the S2I scripts from the specific language image to $STI_SCRIPTS_PATH
COPY ./s2i/bin/ $STI_SCRIPTS_PATH

# Copy extra files to the image.
COPY ./root/ /

# In order to drop the root user, we have to make some directories world
# writeable as OpenShift default security model is to run the container under
# random UID.
RUN mkdir -p ${APP_ROOT}/etc/httpd.d && \
    sed -i -f ${APP_ROOT}/etc/httpdconf.sed /opt/rh/$HTTPD_24/root/etc/httpd/conf/httpd.conf  && \
    chmod -R og+rwx /opt/rh/$HTTPD_24/root/var/run/httpd ${APP_ROOT}/etc/httpd.d && \
    chown -R 1001:0 ${APP_ROOT} && chmod -R ug+rwx ${APP_ROOT} && \
    rpm-file-permissions

USER 1001

# Enable the SCL for all bash scripts.
ENV ENV=${APP_ROOT}/etc/scl_enable \
    PROMPT_COMMAND=". ${APP_ROOT}/etc/scl_enable"

# Set the default CMD to print the usage of the language image
CMD $STI_SCRIPTS_PATH/usage

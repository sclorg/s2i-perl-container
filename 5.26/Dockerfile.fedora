FROM registry.fedoraproject.org/f28/s2i-base:latest

# This image provides a Perl 5.26 environment you can use to run your Perl applications.
EXPOSE 8080

# Image metadata
ENV PERL_VERSION=5.26 \
    PERL_SHORT_VER=526 \
    VERSION=0 \
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
      name="$FGC/$NAME" \
      com.redhat.component="$NAME" \
      version="$VERSION" \
      maintainer="SoftwareCollections.org <sclorg@redhat.com>" \
      help="For more information visit https://github.com/sclorg/s2i-${NAME}-container" \
      usage="s2i build <SOURCE-REPOSITORY> centos/${NAME}-${PERL_SHORT_VER}-centos7:latest <APP-NAME>"

RUN INSTALL_PKGS="perl perl-devel mod_perl perl-CPAN perl-App-cpanminus httpd python2" && \
    dnf install -y --setopt=tsflags=nodocs  $INSTALL_PKGS && \
    rpm -V $INSTALL_PKGS && \
    dnf clean all

# Copy the S2I scripts from the specific language image to $STI_SCRIPTS_PATH
COPY ./s2i/bin/ $STI_SCRIPTS_PATH

# Copy extra files to the image.
COPY ./root/ /

# In order to drop the root user, we have to make some directories world
# writeable as OpenShift default security model is to run the container under
# random UID.
RUN mkdir -p ${APP_ROOT}/etc/httpd.d && \
    sed -i -f ${APP_ROOT}/etc/httpdconf-fed.sed /etc/httpd/conf/httpd.conf  && \
    chmod -R og+rwx /var/run/httpd ${APP_ROOT}/etc/httpd.d && \
    chown -R 1001:0 ${APP_ROOT} && chmod -R ug+rwx ${APP_ROOT} && \
    rpm-file-permissions

# Fedora uses by default 'event' MPM module
# switch to 'prefork' to provide same user experience as with RHEL7 image
# Code taken from 'config_mpm()' function in sclorg/httpd-container repo
ENV HTTPD_MPM=prefork \
    HTTPD_MAIN_CONF_MODULES_D_PATH=/etc/httpd/conf.modules.d

RUN if [ -v HTTPD_MPM -a -f ${HTTPD_MAIN_CONF_MODULES_D_PATH}/00-mpm.conf ]; then \
    mpmconf=${HTTPD_MAIN_CONF_MODULES_D_PATH}/00-mpm.conf; \
    sed -i -e 's,^LoadModule,#LoadModule,' ${mpmconf}; \
    sed -i -e "/LoadModule mpm_${HTTPD_MPM}/s,^#LoadModule,LoadModule," ${mpmconf}; \
    echo "---> Set MPM to ${HTTPD_MPM} in ${mpmconf}"; \
  fi


USER 1001

# Set the default CMD to print the usage of the language image
CMD $STI_SCRIPTS_PATH/usage

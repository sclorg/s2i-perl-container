FROM centos/s2i-base-centos7

# This image provides a Perl 5.20 environment you can use to run your Perl applications.

EXPOSE 8080

# Image metadata
ENV PERL_VERSION=5.20

ENV SUMMARY="Platform for building and running Perl $PERL_VERSION applications" \
    DESCRIPTION="Perl $PERL_VERSION available as docker container is a base platform for \
building and running various Perl $PERL_VERSION applications and frameworks. \
Perl is a high-level programming language with roots in C, sed, awk and shell scripting. \
Perl is good at handling processes and files, and is especially good at handling text. \
Perl's hallmarks are practicality and efficiency. While it is used to do a lot of \
different things, Perl's most common applications are system administration utilities \
and web programming."

LABEL summary="$SUMMARY" \
      description="$DESCRIPTION" \
      io.k8s.description="$DESCRIPTION" \
      io.k8s.display-name="Apache 2.4 with mod_perl/5.20" \
      io.openshift.expose-services="8080:http" \
      io.openshift.tags="builder,perl,perl520" \
      name="centos/perl-520-centos7" \
      com.redhat.component="rh-perl520-docker" \
      version="5.20" \
      release="1" \
      maintainer="SoftwareCollections.org <sclorg@redhat.com>"

# TODO: Cleanup cpanp cache after cpanminus is installed?
RUN yum install -y centos-release-scl && \
    INSTALL_PKGS="rh-perl520 rh-perl520-perl-devel rh-perl520-mod_perl rh-perl520-perl-CPAN" && \
    yum install -y --setopt=tsflags=nodocs $INSTALL_PKGS && \
    rpm -V $INSTALL_PKGS && \
    yum clean all

# Copy the S2I scripts from the specific language image to $STI_SCRIPTS_PATH
COPY ./s2i/bin/ $STI_SCRIPTS_PATH

# Copy extra files to the image.
COPY ./root/ /

# In order to drop the root user, we have to make some directories world
# writeable as OpenShift default security model is to run the container under
# random UID.
RUN mkdir -p /opt/app-root/etc/httpd.d && \
    sed -i -f /opt/app-root/etc/httpdconf.sed /opt/rh/httpd24/root/etc/httpd/conf/httpd.conf  && \
    chmod -R og+rwx /opt/rh/httpd24/root/var/run/httpd /opt/app-root/etc/httpd.d && \
    chown -R 1001:0 /opt/app-root && chmod -R ug+rwx /opt/app-root

USER 1001

# Enable the SCL for all bash scripts.
ENV BASH_ENV=/opt/app-root/etc/scl_enable \
    ENV=/opt/app-root/etc/scl_enable \
    PROMPT_COMMAND=". /opt/app-root/etc/scl_enable"

# Set the default CMD to print the usage of the language image
CMD $STI_SCRIPTS_PATH/usage

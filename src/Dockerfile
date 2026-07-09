FROM {{ spec.s2i_base }}{% if spec.s2i_base_tag %}:{{ spec.s2i_base_tag }}{% endif %}


# This image provides a Perl {{ spec.version }} environment you can use to run your Perl applications.

EXPOSE 8080

# Image metadata
ENV PERL_VERSION={{ spec.version }} \
    PERL_SHORT_VER={{ spec.short }} \
    NAME=perl

ENV SUMMARY="Platform for building and running Perl {{ spec.version }} applications" \
    DESCRIPTION="Perl {{ spec.version }} available as container is a base platform for \
building and running various Perl {{ spec.version }} applications and frameworks. \
Perl is a high-level programming language with roots in C, sed, awk and shell scripting. \
Perl is good at handling processes and files, and is especially good at handling text. \
Perl's hallmarks are practicality and efficiency. While it is used to do a lot of \
different things, Perl's most common applications are system administration utilities \
and web programming."

LABEL summary="$SUMMARY" \
      description="$DESCRIPTION" \
      io.k8s.description="$DESCRIPTION" \
      io.k8s.display-name="Apache 2.4 with mod_fcgid and Perl {{ spec.version }}" \
      io.openshift.expose-services="8080:http" \
      io.openshift.tags="{{ spec.openshift_tags }}" \
      io.openshift.s2i.scripts-url="image:///usr/libexec/s2i" \
      io.s2i.scripts-url="image:///usr/libexec/s2i" \
      name="{{ spec.img_name }}" \
      com.redhat.component="{{ spec.redhat_component }}" \
      com.redhat.license_terms="https://www.redhat.com/en/about/red-hat-end-user-license-agreements#UBI" \
      maintainer="SoftwareCollections.org <sclorg@redhat.com>" \
      help="For more information visit https://github.com/sclorg/s2i-${NAME}-container" \
      usage="s2i build <SOURCE-REPOSITORY> {{ spec.img_name }}:latest <APP-NAME>"

{% if spec.prod == "rhel8" and spec.version == "5.26" %}
# perl-FCGI module is missing a default stream
RUN dnf -y module enable perl-FCGI:0.78
{% endif %}

{% if spec.prod == "rhel8" %}
RUN {{ spec.environment_setup }} && \
    dnf -y --allowerasing distrosync && \
{% else %}
RUN dnf -y --allowerasing distrosync && \
{% endif %}
    INSTALL_PKGS="{{ spec.pkgs}}" && \
    dnf install -y --setopt=tsflags=nodocs $INSTALL_PKGS && \
    perl -v | grep -qe "v$PERL_VERSION\." && echo "Found VERSION {{ spec.version }}" && \
    dnf -y clean all --enablerepo='*'

# Copy the S2I scripts from the specific language image to $STI_SCRIPTS_PATH
COPY ./s2i/bin/ $STI_SCRIPTS_PATH

# Copy extra files to the image.
COPY ./root/ /

# In order to drop the root user, we have to make some directories world
# writeable as OpenShift default security model is to run the container under
# random UID.
RUN mkdir -p ${APP_ROOT}/etc/httpd.d && \
    sed -i -f ${APP_ROOT}/etc/httpdconf.sed /etc/httpd/conf/httpd.conf && \
    chmod -R og+rwx /var/run/httpd /run/mod_fcgid ${APP_ROOT}/etc/httpd.d && \
    chown -R 1001:0 ${APP_ROOT} && chmod -R ug+rwx ${APP_ROOT} && \
    rpm-file-permissions

USER 1001

# Set the default CMD to print the usage of the language image
CMD $STI_SCRIPTS_PATH/usage

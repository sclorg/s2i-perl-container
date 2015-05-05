FROM openshift/base-centos7

# This image provides a Perl 5.16 environment you can use to run your Perl applications.
MAINTAINER  Martin Nagy <mnagy@redhat.com>

# Image metadata
ENV PERL_VERSION=5.16 \
    IMAGE_DESCRIPTION="Perl 5.16" \
    IMAGE_TAGS=perl,perl516 \
    IMAGE_EXPOSE_SERVICES=8080:http \
    PATH=$PATH:/opt/rh/perl516/root/usr/local/bin

# Copy the STI scripts from the specific language image to /usr/local/sti
COPY ./.sti/bin/ /usr/local/sti

# Each language image can have 'contrib' a directory with extra files needed to
# run and build the applications.
COPY ./contrib/ /opt/openshift

# TODO: Cleanup cpanp cache after cpanminus is installed?
RUN yum install -y \
	https://www.softwarecollections.org/en/scls/rhscl/httpd24/epel-7-x86_64/download/rhscl-httpd24-epel-7-x86_64.noarch.rpm \
	https://www.softwarecollections.org/en/scls/rhscl/perl516/epel-7-x86_64/download/rhscl-perl516-epel-7-x86_64.noarch.rpm && \
	yum install -y --setopt=tsflags=nodocs httpd24 perl516 perl516-mod_perl perl516-perl-CPANPLUS && \
	yum clean all && \
	scl enable perl516 -- cpanp 's conf prereqs 1; s save system' && \
	scl enable perl516 -- cpanp 's conf allow_build_interactivity 0; s save system' && \
	scl enable perl516 -- cpanp 'i App::cpanminus' && \
	chown -R default:default /opt/openshift && \
	sed -i -f /opt/openshift/httpdconf.sed /opt/rh/httpd24/root/etc/httpd/conf/httpd.conf  && \
	chmod -R og+rwx /opt/rh/httpd24/root/var/run/httpd

EXPOSE 8080

USER default

# Set the default CMD to print the usage of the language image
CMD ["usage"]

FROM openshift/base-centos7

# This image provides a Perl 5.16 environment you can use to run your Perl applications.
MAINTAINER  Martin Nagy <mnagy@redhat.com>

# Image metadata
ENV PERL_VERSION          5.16
ENV IMAGE_DESCRIPTION     Perl 5.16
ENV IMAGE_TAGS            perl,perl516
ENV IMAGE_EXPOSE_SERVICES 8080:http

RUN yum install -y \
	https://www.softwarecollections.org/en/scls/rhscl/httpd24/epel-7-x86_64/download/rhscl-httpd24-epel-7-x86_64.noarch.rpm \
	https://www.softwarecollections.org/en/scls/rhscl/perl516/epel-7-x86_64/download/rhscl-perl516-epel-7-x86_64.noarch.rpm && \
	yum install -y --setopt=tsflags=nodocs httpd24 perl516 perl516-mod_perl perl516-perl-CPANPLUS && \
	yum clean all

ENV PATH $PATH:/opt/rh/perl516/root/usr/local/bin

# TODO: s save system?
# TODO: Cleanup cpanp cache?
# TODO: We'll need to distribute these....
RUN scl enable perl516 -- cpanp 's conf prereqs 1; s save' && \
	scl enable perl516 -- cpanp 's conf allow_build_interactivity 0; s save' && \
	scl enable perl516 -- cpanp 'i App::cpanminus'

USER default

EXPOSE 8080

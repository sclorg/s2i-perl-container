FROM quay.io/centos7/perl-530-centos7

# Add application sources
ADD app-src \.

# Install dependencies  cpanfile required
RUN cpanm --notest -l extlib Module::CoreList && \
    cpanm --notest -l extlib --installdeps .

RUN printf '\
<Location />\n\
SetHandler perl-script\n\
PerlResponseHandler Plack::Handler::Apache2\n\
PerlSetVar psgi_app app.psgi\n\
</Location>\n' > /opt/app-root/etc/httpd.d/40-psgi.conf

# Run script uses standard ways to run the application
CMD exec httpd -C 'Include /opt/app-root/etc/httpd.conf' -D FOREGROUND

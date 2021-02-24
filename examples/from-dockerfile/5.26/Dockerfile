FROM quay.io/centos7/perl-526-centos7

# Add application sources
ADD app-src \.


# Install dependencies  cpanfile required
RUN cpanm --notest -l extlib Module::CoreList && \
    cpanm --notest -l extlib --installdeps .

CMD sed -i '1i<Location/>' /opt/app-root/etc/httpd.d/40-psgi.conf
CMD sed -i '2iSetHandler perl-script' /opt/app-root/etc/httpd.d/40-psgi.conf
CMD sed -i '3iPerlResponseHandler Plack::Handler::Apache2' /opt/app-root/etc/httpd.d/40-psgi.conf
CMD sed -i '4iPerlSetVar psgi_app app.psgi' /opt/app-root/etc/httpd.d/40-psgi.conf
CMD sed -i '5i</Location>' /opt/app-root/etc/httpd.d/40-psgi.conf
# Run script uses standard ways to run the application
CMD exec httpd -C 'Include /opt/app-root/etc/httpd.conf' -D FOREGROUND

FROM centos/perl-26-centos7

# Add application sources
ADD app-src \.

CMD sed -i '1i<Location/>' /opt/app-root/etc/httpd.d/40-psgi.conf
CMD sed -i '2iSetHandler perl-script' /opt/app-root/etc/httpd.d/40-psgi.conf
CMD sed -i '3iPerlResponseHandler Plack::Handler::Apache2' /opt/app-root/etc/httpd.d/40-psgi.conf
CMD sed -i '4iPerlSetVar psgi_app app.psgi' /opt/app-root/etc/httpd.d/40-psgi.conf
CMD sed -i '5i</Location>' /opt/app-root/etc/httpd.d/40-psgi.conf

# Install dependencies  cpanfile required
RUN export PATH=${PATH}:/opt/rh/rh-perl526/root/usr/bin/&& \
    export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/opt/rh/rh-perl526/root/usr/lib64 && \
    cpanm --notest -l extlib Module::CoreList && \
    cpanm --notest -l extlib --installdeps .

# Run script uses standard ways to run the application
CMD exec httpd -C 'Include /opt/app-root/etc/httpd.conf' -D FOREGROUND

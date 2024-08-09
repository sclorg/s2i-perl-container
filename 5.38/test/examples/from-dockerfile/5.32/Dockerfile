FROM ubi8/perl-532

# Add application sources
ADD app-src .

# Set the paths to local Perl modules
ENV PATH=/opt/app-root/src/extlib/bin:${PATH}
ENV PERL5LIB=/opt/app-root/src/extlib/lib/perl5

# Install the dependencies
RUN  cpanm --notest -l extlib Module::CoreList && \
     cpanm --notest -l extlib --installdeps .

# Install Plack as an FCGI server
RUN cpanm --notest -l extlib Plack::Handler::FCGI FCGI::ProcManager
RUN patch --read-only=ignore -d ./extlib/lib/perl5 -p2 < /opt/app-root/Plack-1.0047-Work-around-mod_fcgid-bogus-SCRIPT_NAME-PATH_INFO.patch
RUN printf '\
FcgidInitialEnv MODFCGID_VIRTUAL_LOCATION /\n\
PassEnv HOME\n\
FcgidInitialEnv "HOME" "%s"\n\
PassEnv PATH\n\
FcgidInitialEnv "PATH" "%s"\n\
PassEnv PERL5LIB\n\
FcgidInitialEnv "PERL5LIB" "%s"\n\
<Location />\n\
SetHandler fcgid-script\n\
Options +ExecCGI\n\
FcgidWrapper "/opt/app-root/psgiwrapper /usr/bin/env plackup -s FCGI ./app.psgi" virtual\n\
</Location>\n' "$HOME" "$PATH" "$PERL5LIB"> /opt/app-root/etc/httpd.d/40-psgi.conf

# Run scripts uses standard ways to run the application
CMD exec httpd -C 'Include /opt/app-root/etc/httpd.conf' -D FOREGROUND

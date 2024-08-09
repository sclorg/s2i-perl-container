FROM ubi9/perl-534

# Add application sources
ADD app-src .

# Set the paths to local Perl modules
ENV PATH=${APP_ROOT}/src/extlib/bin:${PATH}
ENV PERL5LIB=${APP_ROOT}/src/extlib/lib/perl5

# Install the dependencies
RUN  cpanm --notest -l extlib Module::CoreList && \
     cpanm --notest -l extlib --installdeps .

# Install Plack as an FCGI server
RUN cpanm --notest -l extlib Plack::Handler::FCGI FCGI::ProcManager
RUN patch --read-only=ignore -d ./extlib/lib/perl5 -p2 < ${APP_ROOT}/Plack-1.0047-Work-around-mod_fcgid-bogus-SCRIPT_NAME-PATH_INFO.patch
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
FcgidWrapper "${APP_ROOT}/psgiwrapper /usr/bin/env plackup -s FCGI ./app.psgi" virtual\n\
</Location>\n' "$HOME" "$PATH" "$PERL5LIB"> ${APP_ROOT}/etc/httpd.d/40-psgi.conf

# Run scripts uses standard ways to run the application
CMD exec httpd -C 'Include ${APP_ROOT}/etc/httpd.conf' -D FOREGROUND

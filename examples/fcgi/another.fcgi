#!/usr/bin/perl
use FCGI;
my $request = FCGI::Request();
while ($request->Accept() >= 0) {
        print "Content-Type: text/plain\r\n\r\n";
        print "Another FCGI script.\n";
}

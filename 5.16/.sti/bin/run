#!/bin/bash

# For SCL enablement
source .bashrc

set -e

exec httpd -C 'Include /opt/openshift/httpd.conf' -D FOREGROUND

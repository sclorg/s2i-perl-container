#!/bin/bash

set -x

sed -ie 's/old initial value/new initial value/' lib/My/Test.pm
grep 'new initial' lib/My/Test.pm

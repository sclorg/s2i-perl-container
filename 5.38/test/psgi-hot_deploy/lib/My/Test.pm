package My::Test;

use strict;
use warnings;

use Exporter qw(import);

our @EXPORT_OK = qw(test);

sub test {
	my $count = shift;

	return "old initial value: $count\n";
}

1;

#!/usr/bin/perl
#
use Wt2Db;
$WT = new Wt2Db;

$buffer = "foo bar

baz

";

$outbuf = '';

foreach $line (split /\n/, $buffer) {
	$WT->ProcessLine($line);
}
$WT->ProcessEnd();
$outbuf = $WT->Buffer();
print $outbuf;

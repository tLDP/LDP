#!/usr/bin/perl
#
use Wt2Db;
$WT = new Wt2Db;

$buffer = "foo bar

=Section|section=

paragraph

==Subsection|subsection==

paragraph


=Namespaces=

==MailTo==

[[mailto:david@lupercalia.net]]
[[mailto:david@lupercalia.net|David Merrill]]

==HTTP==

[[http://www.tldp.org]]
[[http://www.tldp.org|The Linux Documentation Project]]

";

$outbuf = '';

foreach $line (split /\n/, $buffer) {
	$WT->ProcessLine($line);
}
$WT->ProcessEnd();
$outbuf = $WT->Buffer();
print $outbuf;

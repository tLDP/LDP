#!/usr/bin/perl
#
use Lampadas;
$L = new Lampadas;

if ($L->CurrentUserID()) {
	$L->Redirect('user_home.pl');
} else {
	$L->Redirect('topic_list.pl');
}

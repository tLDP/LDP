#! /usr/bin/perl

use Lampadas;
$L = new Lampadas;

# Read parameters
$user_id	= $L->Param('user_id');
$notes		= $L->Param('notes');

unless ($L->Admin() or ($user_id == $L->CurrentUserID())) {
	$L->Redirect("wrongpermission.pl");
}

$L->AddUserNote($user_id, $notes);
$L->Redirect("user_edit.pl?user_id=$user_id");

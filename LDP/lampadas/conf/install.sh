#!/bin/bash
#
# Installs the configuration file
#

confprefix=/etc

INSTALLCONF="install -p -m 644 --backup=simple"

newconf=N

if [ -f $confprefix/lampadas.conf ]; then
	echo "Installation will overwrite your configuration file,"
	echo "but it will make a backup in lampadas.conf~."
	echo ""
	echo "Do you want to install a new configuration file? (y/n):"
		
	read newconf

	if [ "$newconf" = "y" ]; then
		newconf=Y
	fi

	if [ "$newconf" = "Y" ]; then
		doinstall=Y
	fi
else
	doinstall=Y
fi

if [ "$doinstall" = "Y" ]; then
	$INSTALLCONF lampadas.conf $confprefix/lampadas.conf
	echo "The configuration file was installed."
	if [ "$newconf" = "Y" ]; then
		echo "The backup file is /etc/lampadas.conf~."
	fi
else
	echo "The configuration file was not installed."
fi


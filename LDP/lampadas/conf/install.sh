#!/bin/bash
#
# Installs the configuration file
#

confprefix=/etc/lampadas

INSTALLDIR="install -d"
INSTALLCONF="install -p -m 644 --backup=simple"

$INSTALLDIR $confprefix

# Ask user before overwriting their configuration files.
# 
newconf=N
doinstall=N

if [ -f $confprefix/lampadas.conf ]; then
	echo "Installation will overwrite your lampadas.conf configuration file,"
	echo "but it will make a backup in lampadas.conf~."
	echo ""
	echo "Do you want to install a new lampadas.conf configuration file? (y/n):"
		
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
	echo "The configuration file lampadas.conf was installed."
	if [ "$newconf" = "Y" ]; then
		echo "The backup file is lampadas.conf~."
	fi
else
	echo "The configuration file lampadas.conf was not installed."
fi

# Ask user before overwriting their configuration files.
# 
newconf=N
doinstall=N

if [ -f $confprefix/tidyrc ]; then
	echo "Installation will overwrite your Lampadas tidyrc configuration file,"
	echo "but it will make a backup in tidyrc~."
	echo ""
    echo "NOTE: this does not overwrite your regular /etc/tidyrc file."
    echo ""
	echo "Do you want to install a new tidyrc configuration file? (y/n):"
		
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
	$INSTALLCONF tidyrc $confprefix/tidyrc
	echo "The configuration file tidyrc was installed."
	if [ "$newconf" = "Y" ]; then
		echo "The backup file is tidyrc~."
	fi
else
	echo "The configuration file tidyrc was not installed."
fi


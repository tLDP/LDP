#!/bin/sh
#
# (P) & (C) 2003 - 2011 by Dr. Peter Bieringer <pb@bieringer.de>
#
# Generator script
#
# $Id$
#
# Requires: htmldoc recode docbook-utils-pdf
#
# Changelog
#
# 20020117/PB: review
# 20020128/PB: change PDF generation to LDP conform one, PS is still not LDP conform
# 20070401/PB: disable sgmlfixer (no longer needed)
#              add support for XML file, replace nsgmls by onsgmls
# 20090214/PB: remove </?dummy> tag from SGML, onsgmls don't like it
# 20090523/PB: extend required binary check
# 20091220/PB: catch recode problem
# 20110508/PB: force UTF-8 as input format to fix mixed charset problems in HTML
#              renice whole script
#              support also ldp.dsl stored in same directory as the script
# 20110509/PB: add charset meta header on each html page to force UTF-8

loglevel=6

# parse options
while getopts "ql:" opt; do
	case $opt in
	    q)
		loglevel=4
		;;
	    l)
		loglevel=$OPTARG
		echo "INFO  : set loglevel to: $loglevel"
		;;
	    \?)
		echo "Invalid option: -$OPTARG" >&2
		;;
	esac
done

shift $((OPTIND-1))

if [ -z "$1" ]; then
	file_input="Linux+IPv6-HOWTO.sgml"
	#file_input="Linux+IPv6-HOWTO.xml"
else
	file_input="$1"
fi

if echo "$file_input" | grep -q ".sgml$"; then
	# ok, SGML
	true
elif echo "$file_input" | grep -q ".xml$"; then
	# ok, XML
	true
else
	echo "ERR: file is not a SGML/XML file: $file_input"
	exit 1
fi

if head -1 "$file_input" |grep -q DOCTYPE ; then
	doctype="SGML"
elif head -1 "$file_input" |grep -q "xml version" ; then
	doctype="XML"
else
	echo "ERR: file is not a SGML file: $file_input"
	exit 1
fi

echo "Used SGML file: $file_input"

file_base="${file_input%.*}"

ONSGMLS="/usr/bin/onsgmls"
JADE="/usr/bin/jade"
DB2PS="/usr/bin/db2ps"
DB2PDF="/usr/bin/db2pdf"
LDP_PRINT="/usr/local/bin/ldp_print"
PS2ASCII="/usr/bin/ps2ascii"
RECODE="/usr/bin/recode"
HTMLDOC="/usr/bin/htmldoc"

#LDP_PDFPS="yes"

checklist_bin="ONSGMLS JADE DB2PS DB2PDF PS2ASCII RECODE HTMLDOC"

if [ "$LDP_PDFPS" = "yes" ]; then
	checklist_bin="$checklist_bin LDP_PRINT"
fi


file_ps="$file_base.ps"
file_pdf="$file_base.pdf"
file_txt="$file_base.txt"
file_html="$file_base.html"

file_ldpdsl="/usr/local/share/sgml/dsssl/ldp.dsl"
if [ ! -f $file_ldpdsl ]; then
	# try local stored one
	file_ldpdsl="`dirname $0`"
	if [ "$file_ldpdsl" = "." ]; then
		file_ldpdsl="`pwd`"
	fi
	file_ldpdsl="$file_ldpdsl/ldp.dsl"
fi

file_xmldcl="/usr/share/sgml/xml.dcl"
dir_dssslstylesheets="/usr/share/sgml/docbook/dsssl-stylesheets"

if [ ! -f "$file_ldpdsl" ]; then
	echo "ERR: Missing DSL file: $file_ldpdsl"
	exit 1
fi


if [ ! -f $file_input ]; then
	echo "ERR: Missing SGML file, perhaps export DocBook of LyX won't work"
	exit 1
fi

# look for required files
for f in $file_ldpdsl $file_xmldcl; do
	if [ ! -e $f ]; then
		echo "Missing file: $f"
		exit 1
	fi
done

# look for required binaries
for name in $checklist_bin; do
	f="${!name}"

	if [ ! -e $f ]; then
		echo "Missing file: $f ($name)"
		exit 1
	fi
	if [ ! -x $f ]; then
		echo "Cannot executue: $f ($name)"
		exit 1
	fi
done

# run sgmlfix
#if [ -e ./runsgmlfix.sh ]; then
#	./runsgmlfix.sh "$file_input"
#else
#	echo "WARN: cannot execute 'runsgmlfix.sh'"
#fi

export SP_ENCODING=UTF-8
export SP_CHARSET_FIXED=yes

## Functions
validate_sgml() {
	# remove tags <dummy>, </dummy>
	perl -pi -e 's|</?dummy>||g' "$file_input"

	echo "INFO  : Validate SGML/XML code '$file_input'"
	if [ "$doctype" = "XML" ]; then
		local options="$file_xmldcl"
	fi
	[ $loglevel -ge 7 ] && set -x

	$ONSGMLS -s $options $file_input
	local retval=$?
	[ $loglevel -ge 7 ] && set +x
	if [ $retval -gt 0 ]; then
		echo "ERR: Validation results in errors!"
		return 1
	else
		echo "INFO  : Validation was successfully"
	fi
}

create_html_multipage() {
	echo "INFO  : Create HTML multipages"
	if [ ! -d "$file_base" ]; then
		mkdir "$file_base" || exit 1
	fi
	pushd "$file_base" >/dev/null || exit 1
	rm -f *
	[ $loglevel -ge 7 ] && set -x
	$JADE -t sgml -i html -D $dir_dssslstylesheets -d "${file_ldpdsl}#html" ../$file_input
	local retval=$?
	[ $loglevel -ge 7 ] && set +x

	perl -pi -e 's#><META#><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"\n><META#o' *.html
	local r=$?
	if [ $r -ne 0 ]; then
		retval=$?
	fi

	popd >/dev/null
	return $retval
}

create_html_singlepage() {
	echo "INFO  : Create HTML singlepage '$file_html'"
	[ $loglevel -ge 7 ] && set -x
	$JADE -t sgml -i html -V nochunks -d "${file_ldpdsl}#html" $file_input >$file_html
	local retval=$?
	[ $loglevel -ge 7 ] && set +x

	perl -pi -e 's#><META#><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"\n><META#o' $file_html
	local r=$?
	if [ $r -ne 0 ]; then
		retval=$?
	fi

	if [ $retval -eq 0 ]; then
		echo "INFO  : Create HTML singlepage - done"
	else
		echo "ERR: Create HTML singlepage - an error occurs!"
	fi
	return $retval
}

create_rtf() {
	echo "INFO  : Create RTF file '$file_rtf'"
	[ $loglevel -ge 7 ] && set -x
	$JADE -t rtf -d ${file_ldpdsl} $file_input
	local retval=$?
	[ $loglevel -ge 7 ] && set +x
	if [ $retval -eq 0 ]; then
		echo "INFO  : Create RTF file - done"
	else
		echo "ERR: Create RTF file - an error occurs!"
	fi
	return $retval
}

create_ps() {
	echo "INFO  : Create PS file '$file_ps'"
	[ $loglevel -ge 7 ] && set -x
	$DB2PS --dsl ${file_ldpdsl} $file_input
	local retval=$?
	[ $loglevel -ge 7 ] && set +x
	if [ $retval -eq 0 ]; then
		echo "INFO  : Create PS file - done"
	else
		echo "ERR: Create PS file - an error occurs!"
	fi
	return $retval
}

create_pdf() {
	if [ "$LDP_PDFPS" = "yes" ]; then
		# Use LDP conform mechanism
		echo "INFO  : Create PDF file (LDP conform) '$file_pdf' from HTML file '$file_html'"

		if [ $file_html -ot $file_input ]; then
			echo "ERR: Create PDF file - needed single page HTML file '$file_html' is older than original '$file_input'"
			return 1
		fi
		[ $loglevel -ge 7 ] && set -x
		$LDP_PRINT $file_html
		local retval=$?
		[ $loglevel -ge 7 ] && set +x
	else
		echo "INFO  : Create PDF file (NOT LDP conform) '$file_pdf'"
		[ $loglevel -ge 7 ] && set -x
		$DB2PDF --dsl ${file_ldpdsl} $file_input
		local retval=$?
		[ $loglevel -ge 7 ] && set +x
	fi
	if [ $retval -eq 0 ]; then
		echo "INFO  : Create PDF file - done"
	else
		echo "ERR: Create PDF file - an error occurs!"
	fi
	return $retval
}

create_txt() {
	echo "INFO  : Create TXT file '$file_txt' from PS file '$file_ps'"
	[ -f $file_txt ] && rm $file_txt
	if [ -f $file_ps ]; then
		echo "INFO  : Create TXT file '$file_txt'"
		[ $loglevel -ge 7 ] && set -x
		$PS2ASCII $file_ps > $file_txt
		local retval=$?
		[ $loglevel -ge 7 ] && set +x
	else
		echo "ERR: Cannot create TXT because of missing PS file"
	fi
	if [ $retval -eq 0 ]; then
		echo "INFO  : Create TXT file - done"
	else
		echo "ERR: Create TXT file - an error occurs!"
	fi
	return $retval
}

### Main
validate_sgml
[ $? -ne 0 ] && exit 1

create_html_multipage
if [ $? -ne 0 ]; then
	echo "ERROR : create_html_multipage was not successful"
	exit 1
fi

create_html_singlepage
if [ $? -ne 0 ]; then
	echo "ERROR : create_html_singlepage was not successful"
	exit 1
fi

create_pdf
if [ $? -ne 0 ]; then
	echo "ERROR : create_pdf was not successful"
	exit 1
fi

#create_ps
#[ $? -ne 0 ] && exit 1

#create_txt
#[ $? -ne 0 ] && exit 1

#create_rtf
#[ $? -ne 0 ] && exit 1

## Add VGWort URL
if [ -x ./adjust-html-vgwort.sh ]; then
	case $file_input in
	    'Linux+IPv6-HOWTO.sgml')
		echo "NOTICE: add vgwort URL"
		./adjust-html-vgwort.sh en
		;;
	    'Linux+IPv6-HOWTO.de.sgml')
		echo "NOTICE: add vgwort URL"
		./adjust-html-vgwort.sh de
		;;
	esac
else
	echo "NOTICE : can't add vgwort URL (missing adjust-html-vgwort.sh)"
fi


exit 0

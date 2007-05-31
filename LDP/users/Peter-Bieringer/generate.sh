#!/bin/sh

# 20020117/PB: review
# 20020128/PB: change PDF generation to LDP conform one, PS is still not LDP conform
# 20070401/PB: disable sgmlfixer (no longer needed)
#              add support for XML file, replace nsgmls by onsgmls

# $Id$

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

file_base="${file_input/.*/}"

ONSGMLS="/usr/bin/onsgmls"
JADE="/usr/bin/jade"

file_ps="$file_base.ps"
file_pdf="$file_base.pdf"
file_txt="$file_base.txt"
file_html="$file_base.html"

file_ldpdsl="/usr/local/share/sgml/dsssl/ldp.dsl"
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

LDP_PDFPS="yes"

# look for required files
for f in $file_ldpdsl $file_xmldcl; do
	if [ ! -e $f ]; then
		echo "Missing file: $f"
		exit 1
	fi
done

# look for required binaries
for f in /usr/bin/htmldoc /usr/local/bin/ldp_print $ONSGMLS $JADE /usr/bin/db2ps; do
	if [ ! -e $f ]; then
		echo "Missing file: $f"
		exit 1
	fi
	if [ ! -x $f ]; then
		echo "Cannot executue: $f"
		exit 1
	fi
done

# run sgmlfix
#if [ -e ./runsgmlfix.sh ]; then
#	./runsgmlfix.sh "$file_input"
#else
#	echo "WARN: cannot execute 'runsgmlfix.sh'"
#fi


## Functions
validate_sgml() {
	echo "INF: Validate SGML/XML code '$file_input'"
	if [ "$doctype" = "XML" ]; then
		local options="$file_xmldcl"
	fi
	set -x
	LANG=C $ONSGMLS -s $options $file_input
	local retval=$?
	set +x
	if [ $retval -gt 0 ]; then
		echo "ERR: Validation results in errors!"
		return 1
	else
		echo "INF: Validation was successfully"
	fi
}

create_html_multipage() {
	echo "INF: Create HTML multipages"
	if [ ! -d "$file_base" ]; then
		mkdir "$file_base" || exit 1
	fi
	pushd "$file_base" || exit 1
	rm -f *
	set -x
	LANG=C nice -n 10 $JADE -t sgml -i html -D $dir_dssslstylesheets -d "${file_ldpdsl}#html" ../$file_input
	local retval=$?
	set +x
	popd
	# Force
	#local retval=0
	return $retval
}

create_html_singlepage() {
	echo "INF: Create HTML singlepage '$file_html'"
	set -x
	LANG=C nice -n 10 $JADE -t sgml -i html -V nochunks -d "${file_ldpdsl}#html" $file_input >$file_html
	set +x
	local retval=$?
	if [ $retval -eq 0 ]; then
		echo "INF: Create HTML singlepage - done"
	else
		echo "ERR: Create HTML singlepage - an error occurs!"
	fi
	return $retval
}

create_rtf() {
	echo "INF: Create RTF file '$file_rtf'"
	set -x
	nice -n 10 /usr/bin/jade -t rtf -d /usr/local/share/sgml/ldp.dsl $file_input
	set +x
	local retval=$?
	if [ $retval -eq 0 ]; then
		echo "INF: Create RTF file - done"
	else
		echo "ERR: Create RTF file - an error occurs!"
	fi
	return $retval
}

create_ps() {
	echo "INF: Create PS file '$file_ps'"
	set -x
	nice -n 10 /usr/bin/db2ps --dsl /usr/local/share/sgml/ldp.dsl $file_input
	set +x
	local retval=$?
	if [ $retval -eq 0 ]; then
		echo "INF: Create PS file - done"
	else
		echo "ERR: Create PS file - an error occurs!"
	fi
	return $retval
}

create_pdf() {
	if [ "$LDP_PDFPS" = "yes" ]; then
		# Use LDP conform mechanism
		echo "INF: Create PDF file (LDP conform) '$file_pdf' from HTML file '$file_html'"

		if [ $file_html -ot $file_input ]; then
			echo "ERR: Create PDF file - needed single page HTML file '$file_html' is older than original '$file_input'"
			return 1
		fi
		set -x
		nice -n 10 ldp_print $file_html
		set +x
		local retval=$?
	else
		echo "INF: Create PDF file (NOT LDP conform) '$file_pdf'"
		set -x
		nice -n 10 db2pdf --dsl /usr/local/share/sgml/ldp.dsl $file_input
		set +x
		local retval=$?
	fi
	if [ $retval -eq 0 ]; then
		echo "INF: Create PDF file - done"
	else
		echo "ERR: Create PDF file - an error occurs!"
	fi
	return $retval
}

create_txt() {
	echo "INF: Create TXT file '$file_txt' from PS file '$file_ps'"
	[ -f $file_txt ] && rm $file_txt
	if [ -f $file_ps ]; then
		echo "INF: Create TXT file '$file_txt'"
		set -x
		nice -n 10 ps2ascii $file_ps > $file_txt
		set +x
		local retval=$?
	else
		echo "ERR: Cannot create TXT because of missing PS file"
	fi
	if [ $retval -eq 0 ]; then
		echo "INF: Create TXT file - done"
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

exit 0

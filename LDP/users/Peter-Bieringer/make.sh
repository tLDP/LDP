#!/bin/bash
#
# (P) & (C) 2011 - 2011 by Dr. Peter Bieringer <pb@bieringer.de>
#
# Wrapper script for HOWTO generator script
#
# Requires: "generate.sh"
#
# Changelog
#
#
# 20110511/PB: use absolute paths, extend error checking


URL_BASE="http://cvs.tldp.org/go.to/LDP/LDP/users/Peter-Bieringer/"

FILE_EN="Linux+IPv6-HOWTO.sgml"
FILE_DE="Linux+IPv6-HOWTO.de.sgml"
FILE_FR="Linux+IPv6-HOWTO.fr.sgml"
FILE_PT_BR="Linux+IPv6-HOWTO.pt_BR.sgml"

options_wget="--quiet"

DIR_BASE="$HOME/howtos"
DIR_DOWNLOAD="$HOME/howtos/download"

DIR_DEST_BASE="/var/www/html/howtos"

## logging
log() {
	local level="$1"
	shift

	printf "%-6s: %s\n" "$level" "$*"
}

## download file
download() {
	local url_base="$1"
	local file="$2"

	if [ -z "$url_base" ]; then
		log "ERROR" "'url_base' empty"
		return 1
	fi

	if [ -z "$file" ]; then
		log "ERROR" "'file' empty"
		return 1
	fi

	if [ -z "$DIR_DOWNLOAD" ]; then
		log "ERROR" "no download directory given"
		return 1
	fi

	if [ ! -d "$DIR_DOWNLOAD" ]; then
		log "ERROR" "download directory doesn't exist: $DIR_DOWNLOAD"
		return 1
	fi

	if  [ "$force_download" != "1" ]; then
		log "NOTICE" "skip download $url_base/$file (use option -d)"
		return 0
	fi

	log "INFO" "start download $url_base/$file to directory $DIR_DOWNLOAD"
	wget $options_wget -N -P "$DIR_DOWNLOAD" "$url_base/$file"
	local result=$?
	if [ $result -eq 0 ]; then
		log "INFO" "download successful: $url_base/$file (stored to $DIR_DOWNLOAD)"
	else
		log "ERROR" "download not successful: $url_base/$file"
	fi

	return $result
}

## check, whether processing should be started
check() {
	local file_download="$1"
	local file="$2"
	local dir_html="$3"

	if [ -z "$file" ]; then
		log "ERROR" "'file' empty"
		return 1
	fi

	if [ -z "$file_download" ]; then
		log "ERROR" "'file_download' empty"
		return 1
	fi

	if [ -z "$dir_html" ]; then
		log "ERROR" "'dir_html' empty"
		return 1
	fi

	log "INFO" "check file: $file"

	if [ ! -f "$file_download" ]; then
		log "WARN" "no downloaded file available: $file_download"
		return 1
	fi

	if [ ! -f "$file" ]; then
		log "NOTICE" "no 'old' file available: $file (copy now)"
		cp -p "$file_download" "$file"
		if [ $? -ne 0 ]; then
			log "ERROR" "can't copy 'new' file to 'old' file: $file_download -> $file"
			return 1
		fi

		return 0
	else
		if cmp -s "$file_download" "$file"; then
			log "INFO" "'old' is identical with 'new' file: $file"
		else
			log "NOTICE" "'old' is not equal with 'new' file: $file"
			cp -p "$file_download" "$file"
			if [ $? -ne 0 ]; then
				log "ERROR" "can't copy 'new' file to 'old' file: $file_download -> $file"
				return 1
			fi
			return 0
		fi
		# check contents of destination directory
		log "INFO" "check directory: $dir"

		if [ ! -d "$dir" ]; then
			log "NOTICE" "directory still not exist: $dir"
			return 0
		fi

		local num_files="`find "$dir" -mindepth 1 -maxdepth 1 -type f | wc -l`"
		if [ $num_files -eq 0 ]; then
			# directory is empty
			log "NOTICE" "directory is empty: $dir"
			return 0
		fi

		local num_files_old="`find "$dir" -mindepth 1 -maxdepth 1 -type f ! -newer "$file" | wc -l`"
		if [ $num_files_old -ne 0 ]; then
			# force regeneration
			log "NOTICE" "directory contains old files: $dir ($num_files_old)"
			return 0
		fi
			
		# 'old' file already exists
		if [ "$file" -nt "$file_download" ]; then
			log "WARN" "'old' is newer than 'new' file: $file"
			return 1
		fi
	fi

	if [ "$force_generate" = "1" ]; then
		log "NOTICE" "force regeneration of: $file"
		return 0
	fi

	# nothing to do
	log "DEBUG" "no indication for start processing file found: $file"
	return 1
}

## process/generate output
process() {
	log "INFO" "start processing file: $file"
	pushd $DIR_BASE >/dev/null || return 1
	./generate.sh "$file"
	local result=$?
	popd >/dev/null
	if [ $result -ne 0 ]; then
		log "ERROR" "processing of file not successful: $file"
		return 1
	fi

	log "INFO" "processing of file successful: $file"
}


## copy output
copy() {
	local file="$1"

	if [ -z "$DIR_DEST_BASE" ]; then
		log "ERROR" "destination directory for output not given 'DIR_DEST_BASE'"
	fi
		
	if [ ! -d "$DIR_DEST_BASE" ]; then
		log "ERROR" "destination directory for output doesn't exist: $DIR_DEST_BASE"
		return 1
	fi

	log "INFO" "start syncing files of master file: $file"

	local file_pdf="${file/.sgml/.pdf}"
	local file_html="${file/.sgml/.html}"
	local dir_html="${file/.sgml}"

	local file_base="`basename "${file/.sgml}"`"

	local file_dest_pdf="$DIR_DEST_BASE/${file_base}.pdf"
	local file_dest_html="$DIR_DEST_BASE/${file_base}.html"
	local dir_dest_html="$DIR_DEST_BASE/$file_base"

	local file_dest_status="$DIR_DEST_BASE/${file_base}.last"

	log "INFO" "copy PDF file: $file_pdf"
	cp -p "$file_pdf" "$file_dest_pdf"
	if [ $? -ne 0 ]; then
		log "ERROR" "can't copy PDF file: $file_pdf"
		return 1
	fi

	if [ ! -f "$file_dest_pdf" ]; then
		log "ERROR" "destination PDF file is not a file or doesn't exist: $file_dest_pdf"
		return 1
	fi

	chmod 644 "$file_dest_pdf"
	if [ $? -ne 0 ]; then
		log "ERROR" "can't adjust permissions of PDF file: $file_dest_pdf"
		return 1
	fi

	log "INFO" "copy HTML file: $file_html"
	cp -p "$file_html" "$file_dest_html"
	if [ $? -ne 0 ]; then
		log "ERROR" "can't copy HTML file: $file_html"
		return 1
	fi

	if [ ! -f "$file_dest_html" ]; then
		log "ERROR" "destination HTML file is not a file or doesn't exist: $file_dest_html"
		return 1
	fi

	chmod 644 "$file_dest_html"
	if [ $? -ne 0 ]; then
		log "ERROR" "can't adjust permissions of HTML file: $file_dest_html"
		return 1
	fi

	if [ ! -d "$dir_html" ]; then
		log "ERROR" "source directory for HTML doesn't exist: $dir_html"
		return 1
	fi

	if [ ! -d "$dir_dest_html" ]; then
		log "ERROR" "destination directory for HTML doesn't exist: $dir_dest_html"
		return 1
	fi

	if [ ! -w "$dir_dest_html" ]; then
		log "ERROR" "destination directory for HTML isn't writable: $dir_dest_html"
		return 1
	fi
	log "INFO" "copy HTML directory: $dir_html -> $dir_dest_html"
	rsync --delete -r "$dir_html/" "$dir_dest_html/"
	if [ $? -ne 0 ]; then
		log "ERROR" "can't sync HTML dir: $dir_html"
		return 1
	fi

	log "INFO" "update status file: $file_dest_status"
	touch "$file_dest_status"
	if [ $? -ne 0 ]; then
		log "ERROR" "can't update status file: $file_dest_status"
		return 1
	fi
}





## main
main() {
	for file in $*; do
		download "$URL_BASE" "$file"
		if [ $? -ne 0 ]; then
			continue
		fi

		dir="$DIR_BASE/${file/.sgml}"

		check "$DIR_DOWNLOAD/$file" "$DIR_BASE/$file" "$dir"
		if [ $? -eq 0 ]; then
			process "$DIR_BASE/$file"
		fi

		copy "$DIR_BASE/$file"
	done
}


# parse options
while getopts "dg" opt; do
	case $opt in
	    d)
		force_download=1
		;;
	    g)
		force_download=1
		force_generate=1
		;;
	    \?)
		echo "Invalid option: -$OPTARG" >&2
		;;
	esac
done

shift $((OPTIND-1))

case $1 in
    'de')
	files="$FILE_DE"
	;;
    'en')
	files="$FILE_EN"
	;;
    'fr')
	files="$FILE_FR"
	;;
    'pt')
	files="$FILE_PT_BR"
	;;
    'all')
	files="$FILE_EN $FILE_DE $FILE_FR $FILE_PT_BR"
	;;
esac

main $files

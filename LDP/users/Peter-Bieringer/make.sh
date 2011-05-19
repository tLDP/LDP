#!/bin/bash

URL_BASE="http://cvs.tldp.org/go.to/LDP/LDP/users/Peter-Bieringer/"

FILE_EN="Linux+IPv6-HOWTO.sgml"
FILE_DE="Linux+IPv6-HOWTO.de.sgml"
FILE_FR="Linux+IPv6-HOWTO.fr.sgml"
FILE_PT_BR="Linux+IPv6-HOWTO.pt_BR.sgml"

options_wget="--quiet"
DIR_DOWNLOAD="download"

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
	local file="$1"
	local dir="$2"

	if [ -z "$file" ]; then
		log "ERROR" "'file' empty"
		return 1
	fi

	if [ -z "$dir" ]; then
		log "ERROR" "'dir' empty"
		return 1
	fi

	log "INFO" "check file: $file"

	if [ ! -f "$DIR_DOWNLOAD/$file" ]; then
		log "WARN" "no downloaded file available: $DIR_DOWNLOAD/$file"
		return 1
	fi

	if [ ! -f "$file" ]; then
		log "NOTICE" "no 'old' file available: $file (copy now)"
		cp -p "$DIR_DOWNLOAD/$file" "$file"
		if [ $? -ne 0 ]; then
			log "ERROR" "can't copy 'new' file to 'old' file: $DIR_DOWNLOAD/$file -> $file"
			return 1
		fi

		return 0
	else
		if cmp -s "$file" "$DIR_DOWNLOAD/$file"; then
			log "INFO" "'old' is identical with 'new' file: $file"
		else
			log "NOTICE" "'old' is not equal with 'new' file: $file"
			cp -p "$DIR_DOWNLOAD/$file" "$file"
			if [ $? -ne 0 ]; then
				log "ERROR" "can't copy 'new' file to 'old' file: $DIR_DOWNLOAD/$file -> $file"
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
		if [ "$file" -nt "$DIR_DOWNLOAD/$file" ]; then
			log "WARN" "'old' is newer than 'new' file: $file"
			return 1
		fi
	fi

	# nothing to do
	log "DEBUG" "no indication for start processing file found: $file"
	return 1
}

## process/generate output
process() {
	log "INFO" "start processing file: $file"
	./generate.sh "$file"
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

	log "INFO" "copy PDF file: $file_pdf"
	cp -p "$file_pdf" "$DIR_DEST_BASE/$file_pdf"
	if [ $? -ne 0 ]; then
		log "ERROR" "can't copy PDF file: $file_pdf"
		return 1
	fi
	chmod 644 "$DIR_DEST_BASE/$file_pdf"

	log "INFO" "copy HTML file: $file_html"
	cp -p "$file_html" "$DIR_DEST_BASE/$file_html"
	if [ $? -ne 0 ]; then
		log "ERROR" "can't copy HTML file: $file_html"
		return 1
	fi
	chmod 644 "$DIR_DEST_BASE/$file_html"

	if [ ! -d "$DIR_DEST_BASE/$dir_html" ]; then
		log "ERROR" "destination directory for html doesn't exist: $DIR_DEST_BASE/$dir_html"
		return 1
	fi

	log "INFO" "copy HTML directory: $dir_html -> $DIR_DEST_BASE/$dir_html"
	rsync --delete -r "$dir_html/" "$DIR_DEST_BASE/$dir_html/"
	if [ $? -ne 0 ]; then
		log "ERROR" "can't sync HTML dir: $dir_html"
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

		dir="${file/.sgml}"	

		check "$file" "$dir"
		if [ $? -eq 0 ]; then
			process "$file"
		fi

		copy "$file"
	done
}


# parse options
while getopts "d" opt; do
	case $opt in
	    d)
		# no download
		force_download=1
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

#!/bin/bash
# usage: remove_duplicate_jsons.sh source_dir target_dir
# The script will find the desired files in source_dir 
# and delete it in the target_dir 
# if a duplicate file exists with the same filename
if [ $# -ne 2 ] ; then
    echo "Usage: $0 source_dir target_dir"
    exit 1;
fi

echo "Now running $0 $1 $2"
echo "This script will delete duplicate files which find in $1 and exist in $2"

(cd $1 && find . -type f -name "*.json" -print) | (cut -d/ -f2-) | (cd $2 && while read f; do [ -e "{$f}" ] && echo /bin/rm -f "${f}" && /bin/rm/ -f "${f}"; done;)

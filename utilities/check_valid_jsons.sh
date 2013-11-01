#!/bin/bash
# usage: check whether JSON files are valid in a directory
# The script will judge using 'file' and will treat a JSON
# as unvalid if 'file' reports it's 'data' rather than 'text'

if [ $# -ne 1 ] ; then
    echo "Usage: $0 check_dir"
    exit 1;
fi

echo "Now checking JSON files for $1"
echo "Will check `ls $1/*.json | wc -l` files"
ls $1/*.json | xargs file > $1.check
echo "Done!"
echo "Log file has been saved in $1.check"
echo "There are `less $1.check | grep data | wc -l` unvalid JSON files found"
less $1.check | grep data > $1.unvalid
echo "Unvalid JSON file list has been saved in $1.unvalid"

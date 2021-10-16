#!/bin/bash
set -eu

function usage()
{
    echo "キーワードを含むファイルを検索し、ファイルの内容からハッシュ値を求める"
    echo ""
    echo "$0 \"KEYWORD\" TARGET_DIR"
}


if [ $# -ne 2 ]; then
    usage
    exit 1
fi


KEYWORD=$1
TARGET_DIR=$2
HASH_LIST_FILE=$TARGET_DIR/hash_list.txt
HASH_LIST_SORT_FILE=$TARGET_DIR/hash_list_sort.txt
HASH_LIST_DUP_FILE=$TARGET_DIR/hash_list_dup.txt

if [ ! -d $TARGET_DIR ]; then
    echo "TARGET_DIR is not directory"
    exit 1
fi

if [ -f $HASH_LIST_FILE ]; then
    rm $HASH_LIST_FILE
fi

# キーワードがヒットするファイルを検索
ls $TARGET_DIR/github.com | while read -r line; do
    rg "$KEYWORD" "$TARGET_DIR/github.com/$line" -l --ignore-case | while read -r line2; do
        sha1sum "$line2" | tee -a $HASH_LIST_FILE
    done
done

exit 0

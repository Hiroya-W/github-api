#!/bin/bash
set -eu

function usage()
{
    echo "キーワードで検索でヒットした中から、同じファイルを抽出しリスト化する"
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
    rg "$KEYWORD" $TARGET_DIR/github.com/$line -l --ignore-case | while read -r line2; do
        sha1sum "$line2" | tee -a $HASH_LIST_FILE
    done
done

# 重複するものリストを作成
cat $HASH_LIST_FILE | sort | awk 'colname[$1]++{print}' > $HASH_LIST_DUP_FILE

exit 0

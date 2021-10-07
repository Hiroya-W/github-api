#!/bin/bash
set -eu

function usage()
{
    echo "キーワードで検索した時、同じファイルがヒットした場合、1つのリポジトリを残して、それ以外を削除する"
    echo ""
    echo "$0 KEYWORD TARGET_DIR"
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
rg $KEYWORD $TARGET_DIR -l | sort | while read -r line; do
    sha256sum "$line" >> $HASH_LIST_FILE
done

# 重複するものリストを作成
cat $HASH_LIST_FILE | awk 'colname[$1]++{print}' > $HASH_LIST_DUP_FILE

cat $HASH_LIST_DUP_FILE | while read -r line; do
    # ファイル名を取得
    FILE_NAME=$(echo $line | awk '{print $2}')
    # ファイル名からディレクトリ名を取得
    RM_DIR=$(echo $FILE_NAME | sed -r "s/ghq\/(.+\/github.com\/[^\/]+).*/\1/")
    # ディレクトリを削除
    echo "rm -r ghq/$RM_DIR"
    rm -r ghq/$RM_DIR
done

exit 0

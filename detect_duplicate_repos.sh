#!/bin/bash
set -eu

function usage()
{
    echo "内容が同じファイルを抽出しリスト化する"
    echo ""
    echo "$0 TARGET_DIR"
}


if [ $# -ne 1 ]; then
    usage
    exit 1
fi


TARGET_DIR=$1
HASH_LIST_FILE=$TARGET_DIR/hash_list.txt
HASH_LIST_SORT_FILE=$TARGET_DIR/hash_list_sort.txt
HASH_LIST_DUP_FILE=$TARGET_DIR/hash_list_dup.txt

if [ ! -d $TARGET_DIR ]; then
    echo "TARGET_DIR is not directory"
    exit 1
fi

if [ -f $HASH_LIST_DUP_FILE ]; then
    rm $HASH_LIST_DUP_FILE
fi

cat $HASH_LIST_FILE | sort > $HASH_LIST_SORT_FILE

cat $HASH_LIST_SORT_FILE | awk '{print $1}' | uniq -d | while read -r line; do
    FILES=$(rg "$line" $HASH_LIST_SORT_FILE)
    REPOS=$(echo "$FILES" | awk '{print $2}' | sed -r "s/ghq\/(.+\/github.com\/[^\/]+\/[^\/]+).*/\1/g" | uniq)
    REPO_CNT=$(echo "$REPOS" | wc -l)
    if [ $REPO_CNT -eq 1 ]; then
        echo "$REPOS is skipping"
    else
        # 重複するものリストを作成
        echo "$FILES" | awk 'colname[$1]++{print}' >> $HASH_LIST_DUP_FILE
    fi
done

# cat $HASH_LIST_SORT_FILE | awk 'colname[$1]++{print}' > $HASH_LIST_DUP_FILE

exit 0

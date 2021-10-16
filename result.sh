#!/bin/bash
set -eu

function usage()
{
    echo "リポジトリ一覧と、それらを対象にキーワード検索した結果を出力する"
    echo ""
    echo "$0 \"KEYWORD\" TARGET_DIR"
}


if [ $# -ne 2 ]; then
    usage
    exit 1
fi

KEYWORD=$1
TARGET_DIR=$2
RESULT_TXT=$2/result.txt
RESULT_REPOS=$2/repo-lists.txt

if [ -f "$RESULT_TXT" ]; then
    echo "rm $RESULT_TXT"
    rm "$RESULT_TXT"
fi

if [ -f "$RESULT_REPOS" ]; then
    echo "rm $RESULT_REPOS"
    rm "$RESULT_REPOS"
fi

rg "$KEYWORD" "$TARGET_DIR" -g '!result.txt' --ignore-case | tee -a "$RESULT_TXT"

DIRNAME="$TARGET_DIR"

ls "$DIRNAME/github.com" | while read -r line; do
    echo "$(ls $DIRNAME/github.com/$line)" | while read -r line2; do
        echo "$line/$line2" >> $RESULT_REPOS
    done
done

exit 0

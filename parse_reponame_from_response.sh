#!/bin/bash

function usage()
{
    echo "GitHub REST APIのレスポンスからリポジトリ一覧を取り出す"
    echo ""
    echo "$0 response.json OUTPUT_NAME"
}

if [ $# -ne 2 ]; then
    echo "Invalid number of arguments."
    usage
    exit 1
fi

DIR=repo-lists
DATE=`date '+%Y_%m_%d_%H_%M'`

mkdir -p $DIR

cat $1 \
    | jq '.items[].repository.full_name' \
    | tr -d '"' \
    | sort \
    | uniq > $DIR/$2_$DATE.txt

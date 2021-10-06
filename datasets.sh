#!/bin/bash
set -eu

function usage()
{
    echo "リストから全てのRepositoryをCloneする"
    echo ""
    echo "$0 repo_list.txt"
}

if [ $# -ne 1 ]; then
    usage
    exit 1
fi


repo_list=$1
if [ ! -f $repo_list ]; then
    echo "リストファイルが存在しません"
    exit 1
fi

DIR=`basename $1 .txt`
export GHQ_ROOT=$HOME/Repositories/github.com/Hiroya-W/experiments/ghq/$DIR
cat $1 | ghq get --shallow --parallel

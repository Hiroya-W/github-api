#!/bin/bash
set -eu

ARRAY+=("Here+be+Dragons_C_page_3_2021_10_16_18_13_20")
ARRAY+=("Here+be+Dragons_C_page_4_2021_10_16_18_14_19")
ARRAY+=("Here+be+Dragons_C_page_5_2021_10_16_18_14_47")
ARRAY+=("Here+be+Dragons_C_page_6_2021_10_16_18_15_20")
ARRAY+=("Here+be+Dragons_C_page_7_2021_10_16_18_15_39")
ARRAY+=("Here+be+Dragons_C_page_8_2021_10_16_18_15_56")
ARRAY+=("Here+be+Dragons_C_page_9_2021_10_16_18_16_16")
ARRAY+=("Here+be+Dragons_C_page_10_2021_10_16_18_16_40")

for item in ${ARRAY[@]}; do
    echo "##########"
    echo "RUN: $item"
    echo "##########"
    bash ./datasets.sh repo-lists/$item.txt
    bash ./list_files_contain_keyword.sh "Here Be Dragons" ghq/$item
    bash ./detect_duplicate_repos.sh ghq/$item
    bash ./remove_duplicate_repos.sh ghq/$item/hash_list_dup.txt
    bash ./result.sh "Here Be Dragons" ghq/$item
    echo ""
done

exit 0

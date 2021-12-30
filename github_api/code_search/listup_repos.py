from typing import Any, Dict, List
import hashlib
import re


def extract_fragments(items: Dict[Any, Any], res: List[Any]) -> None:
    for item in items:
        repository_full_name = item.get("repository").get("full_name")
        text_matches = item.get("text_matches")
        for text_match in text_matches:
            object_url = text_match["object_url"]
            fragment = text_match["fragment"]
            fragment_hash = hashlib.sha1(fragment.encode("utf-8")).hexdigest()
            tmp = [repository_full_name, object_url, fragment_hash]
            res.append(tmp)


def has_next_link(response_headers: Dict[Any, Any]) -> bool:
    try:
        link = response_headers["Link"]
        match = re.search(r'<(.*)>; rel="next"', link)
        if match:
            return True
        return False
    except KeyError:
        return False

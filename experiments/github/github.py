import urllib.parse
from typing import Optional

from requests.models import Response

from .session import SessionCore


class GitHubCore:
    BASEURL = "https://api.github.com"

    def __init__(self) -> None:
        sc = SessionCore()
        self._session = sc.session

    def login(self, username: str, password: str) -> None:
        self._session.auth = (username, password)


class GitHub(GitHubCore):
    def search_code(
        self,
        query: str,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
        text_match: bool = False,
    ) -> Response:
        ENDPOINT = "/search/code"
        headers = {"Accept": "application/vnd.github.v3+json"}

        params = _search_code_query_builder(query, per_page, page)

        if text_match:
            headers["Accept"] = "application/vnd.github.v3.text-match+json"

        return self._session.get(
            self.BASEURL + ENDPOINT, params=params, headers=headers
        )


def _search_code_query_builder(
    query: str,
    per_page: Optional[int] = None,
    page: Optional[int] = None,
) -> str:
    params = {"q": query}
    if per_page is not None:
        params["per_page"] = str(per_page)
    if page is not None:
        params["page"] = str(page)

    return urllib.parse.urlencode(params, safe=":")

import urllib.parse
from typing import Optional

from experiments.client import DefaultHttpClient
from requests.models import Response


class GitHubV3(DefaultHttpClient):
    def __init__(self, token: str):
        super().__init__()
        self.__token = token
        self.__rest_url = "https://api.github.com"
        self.__rest_headers = {
            "Authorization": "Bearer {}".format(self.__token),
            "Accept": "application/vnd.github.v3+json",
        }

    def search_code(
        self,
        query: str,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
        text_match: bool = False,
    ) -> Response:
        ENDPOINT = "/search/code"
        headers = self.__rest_headers
        params = _search_code_query_builder(query, per_page, page)

        if text_match:
            headers["Accept"] = "application/vnd.github.v3.text-match+json"

        return self.get(self.__rest_url + ENDPOINT, params=params, headers=headers)


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

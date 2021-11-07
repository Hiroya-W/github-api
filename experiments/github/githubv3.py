import urllib.parse
from typing import Optional

from experiments.client import DefaultHttpClient
from requests.models import Response


class GitHubV3(DefaultHttpClient):
    """
    GitHubV3 is a class that implements the client for the GitHub API v3.

    Examples
    --------
    >>> from experiments.github import get_github_token
    >>> from experiments.github import GitHubV3
    >>>
    >>> gh = GitHubV3(token=get_github_token())
    >>> query = '"KEYWORDS HERE" in:file language:c'
    >>> res = gh.search_code(query, per_page=100, page=10, text_match=True)
    >>> print(res.json())
    """

    def __init__(self, token: str):
        """
        Initializes a new GitHubV3 object.

        Parameters
        ----------
        token: str
            The GitHub API token.
        """
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
        """
        Searches code with the given query.

        Parameters
        ----------
        query: str
            The query to search for.
        per_page: int
            The number of results per page.
        page: int
            The page number.
        text_match: bool
            Whether to search for text matches.

        Returns
        -------
        Response
            The response from the GitHub API.
        """
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
    """
    Builds the query for the search_code method.

    Parameters
    ----------
    query: str
        The query to search for.
    per_page: int
        The number of results per page.
    page: int
        The page number.

    Returns
    -------
    str
        The query.
    """
    params = {"q": query}
    if per_page is not None:
        params["per_page"] = str(per_page)
    if page is not None:
        params["page"] = str(page)

    return urllib.parse.urlencode(params, safe=":")

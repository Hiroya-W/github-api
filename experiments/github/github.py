from requests.models import Response

from .session import SessionCore


class GitHubCore:
    def __init__(self) -> None:
        sc = SessionCore()
        self._session = sc.session

    def login(self, username: str, password: str) -> None:
        self._session.auth = (username, password)


class GitHub(GitHubCore):
    def run(self) -> Response:
        return self._session.get("https://api.github.com/search/code?q=keyword")

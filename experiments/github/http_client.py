from typing import Protocol, Any
from requests.models import Response
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from requests import Session
import json


class HttpClient(Protocol):

    client: Session

    def get(self, url: str) -> Response:
        return self.client.get(url=url)

    def post(self, url: str, body: Any) -> Response:
        return self.client.post(url, json=body.__dict__)


class DefaultHttpClient(HttpClient):
    def __init__(self) -> None:
        retry_strategy = Retry(
            total=3, status_forcelist=[429, 500, 502, 503, 504], backoff_factor=2
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        http = Session()
        http.mount("http://", adapter)
        http.mount("https://", adapter)
        self.client: Session = http

    def get(self, url: str) -> Response:
        return super().get(url)

    def post(self, url: str, body: Any) -> Response:
        return super().post(url, body)


class CustomHttpClient(HttpClient):
    def __init__(self, retry_strategy: Retry) -> None:
        adapter = HTTPAdapter(max_retries=retry_strategy)
        http = Session()
        http.mount("http://", adapter)
        http.mount("https://", adapter)
        self.client: Session = http

    def get(self, url: str) -> Response:
        return super().get(url)

    def post(self, url: str, body: Any) -> Response:
        return super().post(url, body)

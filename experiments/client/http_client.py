from typing import Any, Optional, Protocol

from experiments.client.session import SessionCore
from requests import Session
from requests.adapters import HTTPAdapter
from requests.models import Response
from urllib3.util.retry import Retry


class HttpClient(Protocol):
    def get(
        self, url: str, params: Optional[Any] = None, **kwargs: Optional[Any]
    ) -> Response:
        ...

    def post(
        self,
        url: str,
        data: Optional[Any] = None,
        json: Any = None,
        **kwargs: Optional[Any],
    ) -> Response:
        ...


class DefaultHttpClient(HttpClient):
    def __init__(self) -> None:
        retry_strategy = Retry(
            total=3, status_forcelist=[500, 502, 503, 504], backoff_factor=1
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        http = SessionCore.session
        http.mount("http://", adapter)
        http.mount("https://", adapter)
        self.client = http

    def get(
        self, url: str, params: Optional[Any] = None, **kwargs: Optional[Any]
    ) -> Response:
        return self.client.get(url, params=params, **kwargs)

    def post(
        self,
        url: str,
        data: Optional[Any] = None,
        json: Optional[Any] = None,
        **kwargs: Optional[Any],
    ) -> Response:
        return self.client.post(url, data=data, json=json, **kwargs)


class CustomHttpClient(HttpClient):
    def __init__(self, retry_strategy: Retry) -> None:
        adapter = HTTPAdapter(max_retries=retry_strategy)
        http = SessionCore.session
        http.mount("http://", adapter)
        http.mount("https://", adapter)
        self.client: Session = http

    def get(
        self, url: str, params: Optional[Any] = None, **kwargs: Optional[Any]
    ) -> Response:
        return self.client.get(url, params=params, **kwargs)

    def post(
        self,
        url: str,
        data: Optional[Any] = None,
        json: Optional[Any] = None,
        **kwargs: Optional[Any],
    ) -> Response:
        return self.client.post(url, data=data, json=json, **kwargs)

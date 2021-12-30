from typing import Any, Optional, Protocol

from github_api.client.session import SessionCore
from requests import Session
from requests.adapters import HTTPAdapter
from requests.models import Response
from urllib3.util.retry import Retry


class HttpClient(Protocol):
    """
    HttpClient is a protocol that defines the methods that a client must implement.
    The client is responsible for creating a session and handling the retries.
    """

    def get(
        self, url: str, params: Optional[Any] = None, **kwargs: Optional[Any]
    ) -> Response:
        """
        Get a response from the server.

        Parameters
        ----------
        url : str
            The url to get the response from.
        params : Optional[Any]
            The parameters to pass to the request.
        **kwargs : Optional[Any]
            The keyword arguments to pass to the request.

        Returns
        -------
        Response
            The response from the server.

        Raises
        ------
        requests.exceptions.RequestException
            If the request fails.
        """
        ...

    def post(
        self,
        url: str,
        data: Optional[Any] = None,
        json: Optional[Any] = None,
        **kwargs: Optional[Any],
    ) -> Response:
        """
        Post a request to the server.

        Parameters
        ----------
        url : str
            The url to post the request to.
        data : Optional[Any]
            The data to send to the server.
        json : Any
            The json to send to the server.
        **kwargs : Optional[Any]
            The keyword arguments to pass to the request.

        Returns
        -------
        Response
            The response from the server.

        Raises
        ------
        requests.exceptions.RequestException
            If the request fails.
        """
        ...


class DefaultHttpClient(HttpClient):
    """
    DefaultHttpClient is a class that implements the HttpClient protocol.
    """

    def __init__(self) -> None:
        """
        Initialize the DefaultHttpClient.
        """
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
        """
        Get a response from the server.
        """
        return self.client.get(url, params=params, **kwargs)

    def post(
        self,
        url: str,
        data: Optional[Any] = None,
        json: Optional[Any] = None,
        **kwargs: Optional[Any],
    ) -> Response:
        """
        Post a request to the server.
        """
        return self.client.post(url, data=data, json=json, **kwargs)


class CustomHttpClient(HttpClient):
    def __init__(self, retry_strategy: Retry) -> None:
        """
        Initialize the CustomHttpClient.

        Parameters
        ----------
        retry_strategy : Retry
            The retry strategy to use.
        """
        adapter = HTTPAdapter(max_retries=retry_strategy)
        http = SessionCore.session
        http.mount("http://", adapter)
        http.mount("https://", adapter)
        self.client: Session = http

    def get(
        self, url: str, params: Optional[Any] = None, **kwargs: Optional[Any]
    ) -> Response:
        """
        Get a response from the server.
        """
        return self.client.get(url, params=params, **kwargs)

    def post(
        self,
        url: str,
        data: Optional[Any] = None,
        json: Optional[Any] = None,
        **kwargs: Optional[Any],
    ) -> Response:
        """
        Post a request to the server.
        """
        return self.client.post(url, data=data, json=json, **kwargs)

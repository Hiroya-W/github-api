import time
from typing import Any, Callable, List

from requests.models import Response

DEFAULT_STATUS_CODE = [200]


def retry_requests(
    func: Callable[..., Response],
    sleep_time: int = 60,
    status_code: List[int] = DEFAULT_STATUS_CODE,
    logger: Any = None,
) -> Callable[..., Response]:
    """
    Retry requests.

    Parameters
    ----------
    func : Callable[..., Response]
        Function to be decorated.
    sleep_time : int
        Sleep time in seconds.
    status_code : List[int], optional, default: [200]
        Status codes to be considered as successful.
    logger : Any, optional, default: None
        Logger object.

    Returns
    -------
    Callable[..., Response]
        Decorated function.

    Examples
    --------
    >>> @retry_requests(sleep_time=10)
    >>> def get_repos(url: str) -> Response:
    >>>     return requests.get(url)

    Examples
    --------
    >>> from experiments.github import GitHubV3, get_github_token
    >>>
    >>> gh = GitHubV3(get_github_token())
    >>> search_code = retry_requests(gh.search_code, sleep_time=10)
    >>> query = '"Key Words" in:file language:c'
    >>> res = search_code(query, per_page=1, page=1, text_match=True)
    >>> print(res.json())
    """

    def logwarn(msg: str) -> None:
        if logger is not None:
            logger.warning(msg)
        else:
            print(msg)

    def wrapper(*args: Any, **kwargs: Any) -> Response:
        while True:
            res = func(*args, **kwargs)
            if res.status_code in status_code:
                return res
            elif res.status_code == 404:
                logwarn(f"{res.status_code} error. Skipping. {res.url}")
                return res

            logwarn(f"{res.status_code} error. Retry after {sleep_time} sec.")
            logwarn(f"{res.headers}")
            time.sleep(sleep_time)

    return wrapper

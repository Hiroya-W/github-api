import time
from typing import Any, Callable

from requests.models import Response


def retry_requests(
    func: Callable[..., Response], sleep_time: int = 60, logger: Any = None
) -> Callable[..., Response]:
    """
    Retry requests.

    Parameters
    ----------
    func : Callable[..., Response]
        Function to be decorated.
    sleep_time : int
        Sleep time in seconds.

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

    def wrapper(*args: Any, **kwargs: Any) -> Response:
        while True:
            res = func(*args, **kwargs)
            if res.status_code == 200:
                return res

            if logger is not None:
                logger.warning(
                    f"{res.status_code} error. Retry after {sleep_time} sec."
                )
            else:
                print(f"{res.status_code} error. Retry after {sleep_time} sec.")
            time.sleep(sleep_time)

    return wrapper

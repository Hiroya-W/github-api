# mypy: ignore-errors
from threading import Lock

import requests


class SessionCore:
    _has_instance = None
    _lock = Lock()

    def __new__(cls) -> "SessionCore":
        if not cls._has_instance:
            with cls._lock:
                if not cls._has_instance:
                    cls._has_instance = super(SessionCore, cls).__new__(cls)
            cls.session = cls.create_session()

        return cls._has_instance

    @staticmethod
    def create_session() -> requests.Session:
        return requests.Session()

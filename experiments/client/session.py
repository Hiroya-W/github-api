from threading import Lock
from typing import Any

import requests


class SessionCore:
    _has_instance = None
    _lock = Lock()

    def __new__(cls: Any) -> "SessionCore":
        if not cls._has_instance:
            with cls._lock:
                if not cls._has_instance:
                    cls._has_instance = super(SessionCore, cls).__new__(cls)
            cls.session = requests.Session()

        return cls._has_instance  # type: ignore


SessionCore()

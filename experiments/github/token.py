import os
from logging import getLogger

import keyring

logger = getLogger(__name__)


def set_github_token() -> None:
    GITHUB_TOKEN = keyring.get_password("GitHub-PAT", "Hiroya-W")
    if GITHUB_TOKEN is None:
        GITHUB_TOKEN = ""
    os.environ["GITHUB_TOKEN"] = GITHUB_TOKEN


def get_github_token() -> str:
    if os.environ.get("GITHUB_TOKEN") is None:
        set_github_token()
    return os.environ["GITHUB_TOKEN"]

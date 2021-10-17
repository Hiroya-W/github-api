import os
from logging import getLogger

import keyring

logger = getLogger(__name__)


def set_github_token():
    GITHUB_TOKEN = keyring.get_password("GitHub-PAT", "Hiroya-W")
    os.environ["GITHUB_TOKEN"] = GITHUB_TOKEN

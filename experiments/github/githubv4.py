from experiments.client import DefaultHttpClient
from requests.models import Response


class GitHubV4(DefaultHttpClient):
    def __init__(self, token: str):
        super().__init__()
        self.__token = token
        self.__graphql_url = "https://api.github.com/graphql"
        self.__graphql_headers = {
            "Authorization": "Bearer {}".format(self.__token),
            "Accept": "application/vnd.github.v4+json",
        }

    def query(self, query: str) -> Response:
        response = self.post(
            self.__graphql_url, json={"query": query}, headers=self.__graphql_headers
        )
        return response

    def get_user(self, username: str) -> Response:
        query = (
            """
            query {
                user(login: "%s") {
                    name
                    email
                    bio
                    location
                    avatarUrl
                    url
                    repositories(first: 100) {
                        edges {
                            node {
                                name
                                description
                                url
                                primaryLanguage {
                                    name
                                }
                                stargazers {
                                    totalCount
                                }
                                watchers {
                                    totalCount
                                }
                                forks {
                                    totalCount
                                }
                            }
                        }
                    }
                }
            }
        """
            % username
        )
        return self.query(query)

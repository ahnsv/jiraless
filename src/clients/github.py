from src.clients import HTTPClient, HTTPClientCredential
from src.types import AnyDict, OptionalAnyDict


class GithubPublicClientCredential(HTTPClientCredential):
    def authenticated(self) -> bool:
        return True


class GithubClient(HTTPClient[GithubPublicClientCredential]):
    pass


class GithubIssueV3Client(GithubClient):
    header = {"Accept": "application/vnd.github.v3+json"}
    base_url = "https://api.github.com"

    def request(self, url: str, headers: OptionalAnyDict = None, method: str = "GET") -> AnyDict:
        return super().request(url=f"{self.base_url}/{url}", headers=self.header, method=method)

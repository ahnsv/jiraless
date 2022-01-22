from src.clients import HTTPClient, HTTPClientCredential
from src.types import AnyDict, OptionalAnyDict, OptionalStr


class GithubPublicClientCredential(HTTPClientCredential):
    def authenticated(self) -> bool:
        return True


class GithubPublicClient(HTTPClient[GithubPublicClientCredential]):
    pass


class GithubIssueV3Client(GithubPublicClient):
    header: AnyDict = {"Accept": "application/vnd.github.v3+json"}
    base_url = "https://api.github.com"

    def request(
        self,
        url: str,
        headers: OptionalAnyDict = None,
        method: str = "GET",
        data: OptionalStr = None,
        json: OptionalAnyDict = None,
    ) -> AnyDict:
        if not headers:
            headers = {}
        headers.update(self.header)
        return super().request(
            url=f"{self.base_url}/{url}",
            headers=headers,
            method=method,
            data=data,
            json=json,
        )

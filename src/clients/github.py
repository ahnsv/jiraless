from abc import ABCMeta, abstractmethod, ABC
from typing import List, Union

from src.clients import HTTPClient, HTTPClientCredential, Credential
from src.types import AnyDict, OptionalAnyDict, OptionalStr


class GithubPublicClientCredential(HTTPClientCredential):
    def authenticated(self) -> bool:
        return True


class GithubPrivateClientCredential(HTTPClientCredential):
    def __init__(self, username: str, token: str):
        self.username = username
        self.token = token
        self._authenticated: bool = False

    def authenticated(self) -> bool:
        return self._authenticated

    def authenticate(self) -> AnyDict:
        _header = {
            "Authorization": "token %s" % self.token
        }
        self._authenticated = True
        return _header


class GithubClient(HTTPClient[Credential], ABC, metaclass=ABCMeta):
    def __init__(self, credential: Credential):
        super().__init__(credential=credential)
        self.header: AnyDict = {"Accept": "application/vnd.github.v3+json"}
        self.base_url = "https://api.github.com"

    def request(
            self,
            url: str,
            headers: OptionalAnyDict = None,
            method: str = "GET",
            data: OptionalStr = None,
            json: OptionalAnyDict = None,
    ) -> Union[AnyDict, List[AnyDict]]:
        self.authenticate()
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

    @abstractmethod
    def authenticate(self):
        pass


class GithubPublicClient(GithubClient):
    def authenticate(self):
        pass


class GithubPrivateClient(GithubClient):
    def authenticate(self) -> None:
        header = self.credential.authenticate()
        self.header.update(header)



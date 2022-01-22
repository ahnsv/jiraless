from abc import ABC
from enum import Enum
from typing import TypeVar, Generic

import requests

from src.types import OptionalAnyDict, OptionalStr, AnyDict


class HTTPMethod(str, Enum):
    GET = "get"
    POST = "post"
    PATCH = "patch"


class HTTPClientCredential(ABC):
    def authenticated(self) -> bool:
        ...

    def authenticate(self) -> None:
        ...


Credential = TypeVar('Credential', bound=HTTPClientCredential)


class ClientError(Exception):
    pass


class HTTPClient(ABC, Generic[Credential]):
    def __init__(self, credential: Credential):
        self._client = requests.Session()
        self._credential: HTTPClientCredential = credential

    @property
    def credential(self):
        return self._credential

    def request(self, **kwargs) -> AnyDict:
        return self._request(**kwargs)

    def _request(
            self,
            url: str,
            method: HTTPMethod,
            headers: OptionalAnyDict = None,
            data: OptionalStr = None,
            json: OptionalAnyDict = None,
    ) -> AnyDict:
        if not self._credential.authenticated():
            raise RuntimeError()
        
        response = self._client.request(
            method=method, url=url, headers=headers, data=data, json=json
        )
                       
        if not response.ok:
            raise ClientError()

        return response.json()

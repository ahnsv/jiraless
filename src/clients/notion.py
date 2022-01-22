from dataclasses import dataclass

from src.clients import HTTPClient, HTTPClientCredential
from src.types import AnyDict, OptionalAnyDict, OptionalStr


@dataclass
class NotionClientCredential(HTTPClientCredential):
    api_key: str
    _authenticated: bool = False

    def authenticated(self) -> bool:
        return self._authenticated

    def authenticate(self) -> AnyDict:
        header = {"Authorization": f"Bearer {self.api_key}", "Notion-Version": "2021-08-16"}
        self._authenticated = True
        return header


class NotionClient(HTTPClient):
    base_url = "https://api.notion.com"
    version = "v1"
    header: AnyDict = {"Accept": "application/json"}

    def authenticate(self):
        authentication_header = self.credential.authenticate()
        self.header.update(authentication_header)

    def request(self,
                url: str,
                headers: OptionalAnyDict = None,
                method: str = "GET",
                data: OptionalStr = None,
                json: OptionalAnyDict = None,
                **kwargs) -> AnyDict:
        return super().request(
            url=f"{self.base_url}/{self.version}/{url}",
            headers=headers,
            method=method,
            data=data,
            json=json,
        )





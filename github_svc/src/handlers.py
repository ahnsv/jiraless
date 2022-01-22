import json
import os

from github_svc.src.clients import HTTPClient
from github_svc.src.clients.github import GithubPrivateClientCredential, GithubPrivateClient
from github_svc.src.commands import CreateIssue

credential = GithubPrivateClientCredential(username=os.getenv("GITHUB__USERNAME"), token=os.getenv("GITHUB__TOKEN"))
default_client = GithubPrivateClient(credential=credential)


def create_issue(cmd: CreateIssue, client: HTTPClient = default_client):
    response = client.request(
        url=f"repos/{cmd.repository_owner}/{cmd.repository_name}/issues",
        method="POST",
        data=json.dumps({"title": cmd.title}),
    )
    return response

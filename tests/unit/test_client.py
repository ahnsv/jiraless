import os

import pytest
import json

from src.clients import ClientError
from src.clients.github import GithubPublicClientCredential, GithubPrivateClientCredential, \
    GithubPrivateClient, GithubPublicClient


@pytest.fixture
def github_client():
    credential = GithubPublicClientCredential()
    return GithubPublicClient(credential=credential)


@pytest.fixture
def github_private_client():
    credential = GithubPrivateClientCredential(username=os.getenv("GITHUB__USERNAME"), token=os.getenv("GITHUB__TOKEN"))
    return GithubPrivateClient(credential=credential)


@pytest.mark.parametrize(
    "owner_and_repo",
    [
        ("ahnsv", "grab-lounge-backend", None),
        ("kubernetes", "kubernetes", None),
        ("apache", "airflow", None),
        ("ahnsv", "private repo", ClientError),
    ],
)
def test_github_client_get_issue_list(github_client, owner_and_repo):
    owner, repo, err = owner_and_repo
    try:
        issues = github_client.request(url=f"repos/{owner}/{repo}/issues", method="GET")
        assert issues is not None
    except err:
        assert True


def test_github_client_create_issue(github_private_client: GithubPrivateClient):
    owner, repo = "ahnsv", "jiraless"
    issue = github_private_client.request(
        url=f"repos/{owner}/{repo}/issues",
        method="POST",
        data=json.dumps({"title": "test"}),
    )

    assert issue["state"] == "open"


def test_github_client_update_issue(github_private_client):
    owner, repo, issue_number = "ahnsv", "jiraless", 3
    issue = github_private_client.request(
        url=f"repos/{owner}/{repo}/issues/{issue_number}",
        method="PATCH",
        data=json.dumps({"state": "open"}),
    )
    issue = github_private_client.request(
        url=f"repos/{owner}/{repo}/issues/{issue_number}",
        method="PATCH",
        data=json.dumps({"state": "closed"}),
    )

    assert issue["state"] == "closed"


def test_github_client_get_open_issues_and_close(github_private_client):
    owner, repo = "ahnsv", "jiraless"
    issues = github_private_client.request(
        url=f"repos/{owner}/{repo}/issues", method="GET", data=json.dumps({"state": "open"})
    )
    issue_numbers = [issue["number"] for issue in issues]
    for issue_number in issue_numbers:
        close_response = github_private_client.request(
            url=f"repos/{owner}/{repo}/issues/{issue_number}",
            method="PATCH",
            data=json.dumps({"state": "closed"}),
        )
        assert close_response["state"] == "closed"

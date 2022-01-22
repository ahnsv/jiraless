import pytest
import json

from src.clients import ClientError
from src.clients.github import GithubIssueV3Client, GithubPublicClientCredential


@pytest.fixture
def github_client():
    credential = GithubPublicClientCredential()
    return GithubIssueV3Client(credential=credential)


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


def test_github_client_create_issue(github_client: GithubIssueV3Client):
    owner, repo = "ahnsv", "jiraless"
    issue = github_client.request(
        url=f"repos/{owner}/{repo}/issues",
        method="POST",
        data=json.dumps({"title": "test"}),
    )

    assert issue is None


# def test_github_client_update_issue(github_client):
#     assert False
#
#
# def test_github_client_delete_issue(github_client):
#     assert False

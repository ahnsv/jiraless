import json
import os
import time

import pytest
import redis

from github_svc.src.clients.github import GithubPrivateClientCredential, GithubPrivateClient


@pytest.fixture
def github_private_client():
    credential = GithubPrivateClientCredential(username=os.getenv("GITHUB__USERNAME"), token=os.getenv("GITHUB__TOKEN"))
    return GithubPrivateClient(credential=credential)


@pytest.fixture
def redis_client():
    return redis.Redis(host=os.getenv("REDIS__HOST"), port=os.getenv("REDIS__PORT"))


def test_redis_entrypoint_event_handling(redis_client, github_private_client):
    owner, repo = "ahnsv", "jiraless"
    test_issue_title = "test_entrypoint"
    redis_client.publish(channel="github_svc",
                         message=json.dumps(
                             {"type": "CreateIssue", "title": test_issue_title, "repository_owner": owner,
                              "repository_name": repo}))

    time.sleep(1)
    issues = github_private_client.request(url=f"repos/{owner}/{repo}/issues", method="GET")
    issue_titles = [issue["title"] for issue in issues]
    assert test_issue_title in issue_titles

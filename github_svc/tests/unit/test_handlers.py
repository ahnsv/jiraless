from github_svc.src.commands import CreateIssue
from github_svc.src.messagebus import messagebus


def test_create_issue():
    cmd = CreateIssue(title="test_handler", repository_name="jiraless", repository_owner="ahnsv")
    [result] = messagebus.handle(message=cmd)

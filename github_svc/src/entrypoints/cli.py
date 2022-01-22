import click

from github_svc.src.commands import CreateIssue
from github_svc.src.messagebus import messagebus


@click.group()
def jiraless_github_cli():
    pass


@jiraless_github_cli.command(name="create")
@click.argument("title", type=click.types.STRING)
@click.argument("owner", type=click.types.STRING)
@click.argument("repo_name", type=click.types.STRING)
def create_issue(title: str, owner: str, repo_name: str):
    cmd = CreateIssue(title=title, repository_owner=owner, repository_name=repo_name)
    messagebus.handle(cmd)


if __name__ == '__main__':
    jiraless_github_cli()

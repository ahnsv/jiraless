from pybus.default.messagebus import DefaultMessageBus

from github_svc.src.commands import CreateIssue
from github_svc.src.handlers import create_issue

messagebus = DefaultMessageBus()

messagebus.add_handler(CreateIssue, message_handler=create_issue)

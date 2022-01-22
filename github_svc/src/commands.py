from dataclasses import field

from pybus.core.message import Command
from pydantic import Field


class CreateIssue(Command):
    title: str = Field(default="")
    repository_owner: str = Field(default="")
    repository_name: str = Field(default="")

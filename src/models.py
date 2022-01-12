from datetime import datetime
from typing import Generic, TypeVar
from dataclasses import dataclass, field

T = TypeVar("T")


@dataclass
class TaskEntry(Generic[T]):
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class NotionTaskEntry(TaskEntry):
    pass


@dataclass
class GithubTaskEntry(TaskEntry):
    pass

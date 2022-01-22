import json
import os

import redis

from github_svc.src.commands import CreateIssue
from github_svc.src.messagebus import messagebus

r = redis.Redis(host=os.getenv("REDIS__HOST"), port=os.getenv("REDIS__PORT"))


def handle_external_messages(message: dict):
    print("External Message Received")
    data = json.loads(message["data"])
    message_type = data["type"]

    if message_type == "CreateIssue":
        cmd = CreateIssue(**{k: v for k, v in data.items() if k != "type"})
        messagebus.handle(cmd)
    else:
        raise NotImplementedError()
    print("External Message Handled")


def main():
    pubsub = r.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe("github_svc")

    for message in pubsub.listen():
        handle_external_messages(message)


if __name__ == '__main__':
    main()

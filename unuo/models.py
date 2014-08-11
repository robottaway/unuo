"""Contains core model related code.

Validation, related to the web.
"""
import uuid
import os

from voluptuous import Schema, Required, All, Length
from voluptuous import Optional

from unuo.config import config


build_schema = Schema({
    Required('repo'): All(basestring, Length(min=1, max=1024)),
    Optional('checkout'): All(basestring, Length(min=1, max=256)),
    Required('dockertag'): All(basestring, Length(min=1, max=256)),
    Required('push'): bool
})


class Build():
    """Represents information about a docker build.

    Will contain the Git repo to clone, and the tag to apply to final build.
    """

    def __init__(self, name, repo=None, dockertag='latest', push=False):
        self.name = name
        self.repo = repo
        self.dockertag = dockertag
        self.id = str(uuid.uuid4())
        self.location = os.path.join(config.builds_folder, self.id)
        self.push = push
        self.githash = None

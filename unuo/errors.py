"""Error and exception related code.

"""
import json


class ApiError(Exception):
    """Returned when failure of API.

    Defaults to 400.
    """
    code = 400

    def __init__(self, description, code=None, payload=None):
        Exception.__init__(self)
        self.description = description
        if code is not None:
            self.code = code

    def to_dict(self):
        return {'message': self.description, 'status_code': self.status_code}

    def to_json(self):
        return json.dumps(self.to_dict())


class BuildError(Exception):
    pass

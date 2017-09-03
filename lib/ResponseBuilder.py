from json import dumps

class ResponseBuilder:
    def __init__(self, status=None, body=None):
        self.response = {}

        if not status is None:
            self.status(status)
        if not body is None:
            self.body(body)

    def status(self, status):
        """Set the response status."""
        if not isinstance(status) is int:
            raise TypeError("Response status not an int")

        self.response["status"] = status
        return self

    def header(self, key, value):
        """Add a header to the response"""
        if not isinstance(key) is str:
            raise TypeError("Header key is not a string")
        if not isinstance(value) is str:
            raise TypeError("Header value is not a string")
        if "headers" not in self.response:
            self.response["headers"] = {}

        self.response["headers"][key] = value
        return self

    def body(self, body):
        """Set the response body."""
        self.response["body"] = body
        return self

    def build(self):
        """Returns the response."""
        return self.response

    def json(self):
        """Returns the response as a json string."""
        return dumps(self.response)

def OK(body=None):
    return ResponseBuilder(200, body)

def BadRequest(body=None):
    return ResponseBuilder(400, body)

def NotFound(body=None):
    return ResponseBuilder(404, body)

def ServerError(body=None):
    return ResponseBuilder(500, body)

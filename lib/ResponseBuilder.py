from json import dumps

__author__ = 'Rudolf Stander'
__contact__ = 'rudolfstan@gmail.com'
__see__ = 'https://github.com/RudolfStander/aws-lambdas'

class ResponseBuilder:
    """
    TODO: Proper intro comment

    A response should have the following form:

    {
        "status": integer, valid HTTP status code,
        "headers": dictionary (optional),
        "body": any json serializable object, including None (optional)
    }

    The status field should contain a valid HTTP status code.
    The headers are optional, but can be used to give the caller some additional info.
    The body carries the payload of the response.
    """

    def __init__(self, status=None, headers=None, body=None):
        # TODO: comment arguments
        self.response = {}

        if not status is None:
            self.status(status)
        if not headers is None:
            if not isinstance(headers, list):
                raise TypeError("Headers should contain a list of key-value pairs")

            for entry in headers:
                if not isinstance(entry, tuple):
                    raise TypeError("Header entry not a tuple")
                if len(entry) != 2:
                    raise TypeError("Header entry does not have exactly two elements")

                self.header(entry[0], entry[1])
        if not body is None:
            self.body(body)

    def status(self, status):
        """Set the response status."""
        if not isinstance(status, int):
            raise TypeError("Response status not an int")

        self.response["status"] = status
        return self

    def header(self, key, value):
        """Add a header to the response"""
        if not isinstance(key, str):
            raise TypeError("Header key is not a string")
        if not isinstance(value, str):
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
        """Returns the response if it has a valid status."""
        if "status" not in self.response:
            raise KeyError("No status defined for response")

        return self.response

    def json(self):
        """Returns the response as a json string."""
        if "status" not in self.response:
            raise KeyError("No status defined for response")

        # TODO: DynamoDB returns Decimal for numeric values, but it is not JSON serializable,
        #       so either extend the serializer, OR
        #       recursively check if there is a Decimal value, OR
        #       let the lambda handle it (probably the best option)

        return dumps(self.response)

def OK(body=None):
    return ResponseBuilder(status=200, body=body)

def BadRequest(body=None):
    return ResponseBuilder(status=400, body=body)

def NotFound(body=None):
    return ResponseBuilder(status=404, body=body)

def ServerError(body=None):
    return ResponseBuilder(status=500, body=body)

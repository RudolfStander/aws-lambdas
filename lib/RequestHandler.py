class RequestHandler:
    """
    TODO: Proper intro comment

    A request should have the following form:

    {
        "type": string,
        "headers": dictionary (optional),
        "body": dictionary (optional)
    }

    The type field will be used to identify the handling function to be used.
    The headers are optional, but can be used to give the RequestHandler some additional info.
    The body carries the payload of the request.

    Every handle method should return a response in the form of:

    {
        "status": int,
        "headers: dictionary (optional),
        "body": dictionary
    }

    The status should be a valid HTTP status code.
    The headers are optional, but can be used to give the receiver some additional info.
    The body carries the payload of the response. In the event that the response is an error,
    the body could contain an error message
    """

    def __init__(self):
        # A map of request type to request validator function
        self.validators = {}
        # A map of request type to request handler function
        self.handlers = {}

    def validate(self, request):
        """
        Applies some validation to the base request before passing the request to
        a type specific validator, if one was defined.
        """
        if request is None:
            raise ValueError("The request is empty")
        if "type" not in request or request["type"] is None:
            raise ValueError("No type field on request")
        if not isinstance(request["type"]) is str:
            raise ValueError("Type field is not a string")
        if request["type"] not in self.handlers:
            raise NotImplementedError("No handler for request type found")
        if request["type"] in self.validators:
            self.validators[request["type"]](request)

    def handle(self, request):
        """Validates and handles the request."""
        self.validate(request)
        self.handlers[request["type"]](request)

    def add_validator(self, request_type, validator):
        """
        Add a validator function to the list of type specific validators.

        A Validator takes a request and should raise exceptions if the request does not conform to
        the expected format for the specific request type.

        Validation is performed before attempting to handle the request.
        """
        self.validators[request_type] = validator

    def add_handler(self, request_type, handler):
        """
        Add a handler function to the list of type specific handlers.

        A Handler takes a request and should return a valid response.
        """
        self.handlers[request_type] = handler

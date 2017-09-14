from ..lib.DB import DB
from ..lib.ResponseBuilder import OK, BadRequest, ServerError, NotFound
from ..lib.RequestHandler import RequestHandler

__author__ = 'Rudolf Stander'
__contact__ = 'rudolfstan@gmail.com'
__see__ = 'https://github.com/RudolfStander/aws-lambdas'

class CRUDHandler(RequestHandler):
    """
      TODO: comment
    """

    def __init__(self, db=None, table_name=None, test=False):
        RequestHandler.__init__(self)

        if not table_name is None:
            self._db = DB(table_name, test)
        elif not db is None:
            self._db = db

        self.add_validator("GET", self.get_validator)
        self.add_handler("GET", self.get_handler)
        self.add_validator("PUT", self.put_validator)
        self.add_handler("PUT", self.put_handler)
        self.add_validator("SCAN", self.scan_validator)
        self.add_handler("SCAN", self.scan_handler)
        self.add_validator("DELETE", self.delete_validator)
        self.add_handler("DELETE", self.delete_handler)
        self.add_validator("CREATE", self.create_validator)
        self.add_handler("CREATE", self.create_handler)
        self.add_validator("UPDATE", self.update_validator)
        self.add_handler("UPDATE", self.update_handler)

    def handle(self, request):
        print("request: ", request)

        try:
            return RequestHandler.handle(self, request).json()
        except ValueError as value_error:
            return BadRequest(value_error.message).json()
        except TypeError as type_error:
            return ServerError(type_error.message).json()
        except KeyError as k_error:
            return ServerError(k_error.message).json()
        except NotImplementedError as ni_error:
            return ServerError(ni_error.message).json()
        except Exception as error:
            return ServerError(error.message).json()

    def get_validator(self, request):
        if "body" not in request or request["body"] is None:
            raise ValueError("No body in GET request")

    def get_handler(self, request):
        if self._db is None:
            raise UnboundLocalError("No DB class was instantiated")

        db_response = self._db.get(request["body"])

        if db_response is None or not isinstance(db_response, dict) or not db_response:
            return NotFound()

        return OK(db_response)

    def put_validator(self, request):
        if "body" not in request or request["body"] is None:
            raise ValueError("No body in PUT request")

    def put_handler(self, request):
        if self._db is None:
            raise UnboundLocalError("No DB class was instantiated")

        db_response = self._db.put(request["body"])

        return OK(db_response)

    def scan_validator(self, request):
        if "body" in request and not request["body"] is None:
            if "limit" in request and not isinstance(request["limit"], int):
                raise ValueError("Invalid type for 'limit' field in SCAN request")
            if "start_key" in request and not isinstance(request["start_key"], dict):
                raise ValueError("Invalid type for 'start_key' field in SCAN request")

    def scan_handler(self, request):
        if self._db is None:
            raise UnboundLocalError("No DB class was instantiated")

        limit = None
        start_key = None

        if "limit" in request:
            limit = request["limit"]
        if "start_key" in request:
            start_key = request["start_key"]

        db_response = self._db.scan(limit=limit, start_key=start_key)

        if db_response is None or not isinstance(db_response[0], list) or not db_response[0]:
            return NotFound()

        if not db_response[1] is None:
            return OK({
                "items": db_response[0],
                "last_key": db_response[1]
            })
        else:
            return OK({
                "items": db_response[0],
            })

    def delete_validator(self, request):
        if "body" not in request or request["body"] is None:
            raise ValueError("No body in GET request")

    def delete_handler(self, request):
        if self._db is None:
            raise UnboundLocalError("No DB class was instantiated")

        db_response = self._db.delete(request["body"])

        return OK(db_response)

    def create_validator(self, request):
        raise NotImplementedError("TODO, implement create_validator")

    def create_handler(self, request):
        raise NotImplementedError("TODO, implement create_handler")

    def update_validator(self, request):
        raise NotImplementedError("TODO, implement update_validator")

    def update_handler(self, request):
        raise NotImplementedError("TODO, implement update_handler")

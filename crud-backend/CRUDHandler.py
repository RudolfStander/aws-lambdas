from ..lib.DB import DB
from ..lib.ResponseBuilder import OK, BadRequest, ServerError, NotFound
from ..lib.RequestHandler import RequestHandler

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
        self.add_validator("GET_ALL", self.get_all_validator)
        self.add_handler("GET_ALL", self.get_all_handler)
        self.add_validator("CREATE", self.create_validator)
        self.add_handler("CREATE", self.create_handler)
        self.add_validator("UPDATE", self.update_validator)
        self.add_handler("UPDATE", self.update_handler)
        self.add_validator("DELETE", self.delete_validator)
        self.add_handler("DELETE", self.delete_handler)

    def handle(self, request):
        try:
            return RequestHandler.handle(self, request)
        except ValueError as value_error:
            return BadRequest(value_error.message)
        except TypeError as type_error:
            return ServerError(type_error.message)
        except KeyError as k_error:
            return ServerError(k_error.message)
        except NotImplementedError as ni_error:
            return ServerError(ni_error.message)
        except Exception as error:
            return ServerError(error.message)

    def get_validator(self, request):
        if "body" not in request or request["body"] is None:
            raise ValueError("No body in GET request")

    def get_handler(self, request):
        if self._db is None:
            raise UnboundLocalError("No DB class was instantiated")

        db_response = self._db.get(request["body"])

        if db_response is None or not isinstance(db_response) is dict or not db_response:
            return NotFound()

        return OK(db_response)

    def get_all_validator(self, request):
        raise NotImplementedError("TODO, implement get_all_validator")

    def get_all_handler(self, request):
        raise NotImplementedError("TODO, implement get_all_handler")

    def create_validator(self, request):
        raise NotImplementedError("TODO, implement create_validator")

    def create_handler(self, request):
        raise NotImplementedError("TODO, implement create_handler")

    def update_validator(self, request):
        raise NotImplementedError("TODO, implement update_validator")

    def update_handler(self, request):
        raise NotImplementedError("TODO, implement update_handler")

    def delete_validator(self, request):
        raise NotImplementedError("TODO, implement delete_validator")

    def delete_handler(self, request):
        raise NotImplementedError("TODO, implement delete_handler")

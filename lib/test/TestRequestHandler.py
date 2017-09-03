import unittest
from ..RequestHandler import RequestHandler

class TestRequestHandler(unittest.TestCase):
    def setUp(self):
        self.handler = RequestHandler()

    def test_base_validation(self):
        self.assertRaises(ValueError, self.empty_request)
        self.assertRaises(ValueError, self.no_type_field)
        self.assertRaises(ValueError, self.empty_type_field)
        self.assertRaises(ValueError, self.non_string_type_field)
        self.assertRaises(NotImplementedError, self.no_handler)

    def empty_request(self):
        self.handler.validate(None)

    def no_type_field(self):
        request = {}
        self.handler.validate(request)

    def empty_type_field(self):
        request = {
            "type": None
        }
        self.handler.validate(request)

    def non_string_type_field(self):
        request = {
            "type": []
        }
        self.handler.validate(request)

    def no_handler(self):
        request = {
            "type": "some_operation"
        }
        self.handler.validate(request)

    def valdate_stuff(self, request):
        if "body" not in request:
            raise ValueError("Body not in request")

    def test_additional_validator(self):
        self.handler.add_handler("stuff", None) # Need this to bypass handler check
        self.handler.add_validator("stuff", self.valdate_stuff)
        self.assertRaises(ValueError, self.no_stuff_in_request)

        try:
            self.stuff_in_request()
        except Exception:
            self.fail()

    def no_stuff_in_request(self):
        request = {
            "type": "stuff"
        }
        self.handler.validate(request)

    def stuff_in_request(self):
        request = {
            "type": "stuff",
            "body": None
        }
        self.handler.validate(request)

    def test_custom_handler(self):
        self.handler.add_handler("stuff", self.handle_stuff)

        body = "stuff in body"
        request = {
            "type": "stuff",
            "body": body
        }

        result = self.handler.handle(request)

        if result != body:
            self.fail()

    def handle_stuff(self, request):
        if not request is None:
            return request["body"]
        else:
            return None

if __name__ == "__main__":
    unittest.main()

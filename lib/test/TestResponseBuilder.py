import unittest
from ..ResponseBuilder import ResponseBuilder

class TestResponseBuilder(unittest.TestCase):
    def setUp(self):
        self.builder = ResponseBuilder()
        self.assertIsNotNone(self.builder.response)

    def test_status(self):
        self.builder.status(200)
        self.assertIn("status", self.builder.response)
        self.assertEqual(200, self.builder.response["status"])

    def test_status_invalid(self):
        self.assertRaises(TypeError, self.builder.status, "200")

    def test_header(self):
        self.builder.header("key", "value")
        self.assertIn("headers", self.builder.response)
        self.assertIn("key", self.builder.response["headers"])
        self.assertEqual("value", self.builder.response["headers"]["key"])

    def test_header_invalid_key(self):
        self.assertRaises(TypeError, self.builder.header, None, "value")
        self.assertRaises(TypeError, self.builder.header, 1, "value")

    def test_header_invalid_value(self):
        self.assertRaises(TypeError, self.builder.header, "key", None)
        self.assertRaises(TypeError, self.builder.header, "key", 1)

    def test_body(self):
        self.builder.body("stuff")
        self.assertIn("body", self.builder.response)
        self.assertEqual("stuff", self.builder.response["body"])

    def test_build(self):
        response = self.builder.status(200).build()
        self.assertIn("status", response)
        self.assertEqual(200, response["status"])

    def test_build_no_status_defined(self):
        self.assertRaises(KeyError, self.builder.build)

    def test_json(self):
        json = self.builder.status(200).json()
        self.assertIsInstance(json, str)
        self.assertEqual("{\"status\":200}", json.replace(" ", ""))

    def test_json_no_status_defined(self):
        self.assertRaises(KeyError, self.builder.json)

    def test_init_with_status(self):
        self.builder = ResponseBuilder(200)
        self.assertIn("status", self.builder.response)
        self.assertEqual(200, self.builder.response["status"])

    def test_init_with_body(self):
        self.builder = ResponseBuilder(body="stuff")
        self.assertIn("body", self.builder.response)
        self.assertEqual("stuff", self.builder.response["body"])

    def test_init_with_single_header(self):
        self.builder = ResponseBuilder(headers=[("key", "value")])
        self.assertIn("headers", self.builder.response)
        self.assertIn("key", self.builder.response["headers"])
        self.assertEqual("value", self.builder.response["headers"]["key"])

    def test_init_with_multiple_headers(self):
        self.builder = ResponseBuilder(headers=[("key", "value"), ("key2", "value2")])
        self.assertIn("headers", self.builder.response)
        self.assertIn("key", self.builder.response["headers"])
        self.assertEqual("value", self.builder.response["headers"]["key"])
        self.assertIn("key2", self.builder.response["headers"])
        self.assertEqual("value2", self.builder.response["headers"]["key2"])

    def test_init_with_invalid_header(self):
        self.assertRaises(TypeError, self.init_with_non_list_type_header)
        self.assertRaises(TypeError, self.init_with_non_tuple_entry_header)
        self.assertRaises(TypeError, self.init_with_single_element_tuple_header)
        self.assertRaises(TypeError, self.init_with_too_many_element_tuple_header)

    def init_with_non_list_type_header(self):
        self.builder = ResponseBuilder(headers="key-value")

    def init_with_non_tuple_entry_header(self):
        self.builder = ResponseBuilder(headers=["key-value"])

    def init_with_single_element_tuple_header(self):
        self.builder = ResponseBuilder(headers=[("key-value")])

    def init_with_too_many_element_tuple_header(self):
        self.builder = ResponseBuilder(headers=[("key", "value", "nonsense")])

if __name__ == "__main__":
    unittest.main()

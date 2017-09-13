import unittest
import boto3
from json import loads

from ..CRUDHandler import CRUDHandler

# Get the service resource.
dynamodb = boto3.resource("dynamodb", region_name="eu-west-1", endpoint_url="http://localhost:8000",
                          aws_access_key_id="anything", aws_secret_access_key="anything")

def setup_dynamo_db(table_name):
    # Create the DynamoDB table.
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                "AttributeName": "id",
                "KeyType": "HASH"
            },
            {
                "AttributeName": "word",
                "KeyType": "RANGE"
            }
        ],
        AttributeDefinitions=[
            {
                "AttributeName": "id",
                "AttributeType": "S"
            },
            {
                "AttributeName": "word",
                "AttributeType": "S"
            }
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5
        }
    )

    # Wait until the table exists.
    table.meta.client.get_waiter("table_exists").wait(TableName=table_name)

def tear_down_dynamo_db(table_name):
    table = dynamodb.Table(table_name)
    table.delete()

class TestLambda(unittest.TestCase):
    def setUp(self):
        self.table_name = "TestDB"
        print("==== Start test ====")
        setup_dynamo_db(self.table_name)
        self.handler = CRUDHandler(table_name=self.table_name, test=True)

    def tearDown(self):
        tear_down_dynamo_db(self.table_name)
        print("==== End test ====\n")

    def test_put_and_get(self):
        new_item = {
            "id": "1",
            "word": "random",
            "number_as_string": "42"
        }
        request = {
            "type": "PUT",
            "body": new_item
        }

        response = self.handler.handle(request)
        self.assertIsNotNone(response)

        response = loads(response)
        self.assertEqual(200, response["status"])

        item_key = {
            "id": "1",
            "word": "random"
        }
        request = {
            "type": "GET",
            "body": item_key
        }

        response = self.handler.handle(request)
        self.assertIsNotNone(response)

        response = loads(response)
        self.assertEqual(200, response["status"])
        self.assertIn("body", response)
        self.assertEqual("1", response["body"]["id"])
        self.assertEqual("random", response["body"]["word"])
        self.assertEqual("42", response["body"]["number_as_string"])

    def test_delete(self):
        new_item = {
            "id": "1",
            "word": "random",
            "number_as_string": "42"
        }
        request = {
            "type": "PUT",
            "body": new_item
        }

        response = self.handler.handle(request)
        self.assertIsNotNone(response)

        response = loads(response)
        self.assertEqual(200, response["status"])

        item_key = {
            "id": "1",
            "word": "random"
        }

        request = {
            "type": "DELETE",
            "body": item_key
        }

        response = self.handler.handle(request)
        self.assertIsNotNone(response)

        response = loads(response)
        self.assertEqual(200, response["status"])

        request = {
            "type": "GET",
            "body": item_key
        }

        response = self.handler.handle(request)
        self.assertIsNotNone(response)

        response = loads(response)
        self.assertEqual(404, response["status"])

    def test_scan(self):
        new_item = {
            "id": "1",
            "word": "random",
            "number_as_string": "42"
        }
        request = {
            "type": "PUT",
            "body": new_item
        }

        response = self.handler.handle(request)
        self.assertIsNotNone(response)

        new_item = {
            "id": "2",
            "word": "something",
            "number_as_string": "13"
        }
        request["body"] = new_item

        response = self.handler.handle(request)
        self.assertIsNotNone(response)

        request = {
            "type": "SCAN"
        }

        response = self.handler.handle(request)
        self.assertIsNotNone(response)

        response = loads(response)
        self.assertEqual(200, response["status"])
        self.assertIn("body", response)
        self.assertIn("items", response["body"])
        self.assertEqual(2, len(response["body"]["items"]))

    def test_put_invalid_body(self):
        self.fail()

    def test_put_invalid_item_key(self):
        self.fail()

    def test_get_invalid_body(self):
        self.fail()

    def test_get_invalid_item_key(self):
        self.fail()

    def test_delete_invalid_body(self):
        self.fail()

    def test_delete_invalid_item_key(self):
        self.fail()

    def test_scan_invalid_limit(self):
        self.fail()

    def test_scan_invalid_start_key(self):
        self.fail()

if __name__ == "__main__":
    unittest.main()

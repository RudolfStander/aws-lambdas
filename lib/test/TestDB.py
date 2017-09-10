import unittest
import boto3
from ..DB import DB

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

class TestDB(unittest.TestCase):
    def setUp(self):
        self.table_name = "TestDB"
        print("==== Start test ====")
        setup_dynamo_db(self.table_name)

    def tearDown(self):
        tear_down_dynamo_db(self.table_name)
        print("==== End test ====\n")

    def test_put_and_get(self):
        db = DB(self.table_name, test=True)

        item = {
            "id": "1",
            "word": "random",
            "number": 42
        }
        db.put(item)

        get_key = {
            "id": "1",
            "word": "random"
        }
        db_response = db.get(get_key)

        self.assertIsNotNone(db_response)
        self.assertIn("id", db_response)
        self.assertEqual("1", db_response["id"])
        self.assertIn("word", db_response)
        self.assertEqual("random", db_response["word"])
        self.assertIn("number", db_response)
        self.assertEqual(42, db_response["number"])

    def test_put_as_update(self):
        db = DB(self.table_name, test=True)

        item = {
            "id": "1",
            "word": "random",
            "number": 42
        }
        db.put(item)

        item["number"] = 43
        db.put(item)

        get_key = {
            "id": "1",
            "word": "random"
        }
        db_response = db.get(get_key)

        self.assertIsNotNone(db_response)
        self.assertIn("id", db_response)
        self.assertEqual("1", db_response["id"])
        self.assertIn("word", db_response)
        self.assertEqual("random", db_response["word"])
        self.assertIn("number", db_response)
        self.assertEqual(43, db_response["number"])

    def test_delete(self):
        db = DB(self.table_name, test=True)

        item = {
            "id": "1",
            "word": "random",
            "number": 42
        }
        db.put(item)

        key = {
            "id": "1",
            "word": "random"
        }
        db_response = db.delete(key)
        db_response = db.get(key)

        self.assertIsNone(db_response)

    def test_simple_scan(self):
        db = DB(self.table_name, test=True)

        item = {
            "id": "1",
            "word": "random",
            "number": 42
        }
        db.put(item)

        db_response = db.scan()

        self.assertIsNotNone(db_response)
        self.assertIsNotNone(db_response[0])
        self.assertIsNone(db_response[1])

        items = db_response[0]

        self.assertEqual(1, len(items))
        self.assertIn("id", items[0])
        self.assertEqual("1", items[0]["id"])
        self.assertIn("word", items[0])
        self.assertEqual("random", items[0]["word"])
        self.assertIn("number", items[0])
        self.assertEqual(42, items[0]["number"])

    def test_scan_with_limit(self):
        db = DB(self.table_name, test=True)

        item = {
            "id": "1",
            "word": "random",
            "number": 42
        }
        db.put(item)
        item = {
            "id": "2",
            "word": "not",
            "number": 36
        }
        db.put(item)

        db_response = db.scan(limit=1)

        self.assertIsNotNone(db_response)
        self.assertIsNotNone(db_response[0])
        self.assertIsNotNone(db_response[1])

        items = db_response[0]

        self.assertEqual(1, len(items))
        self.assertIn("id", items[0])
        self.assertEqual("1", items[0]["id"])
        self.assertIn("word", items[0])
        self.assertEqual("random", items[0]["word"])
        self.assertIn("number", items[0])
        self.assertEqual(42, items[0]["number"])

        self.assertIn("id", db_response[1])
        self.assertEqual("1", db_response[1]["id"])
        self.assertIn("word", db_response[1])
        self.assertEqual("random", db_response[1]["word"])

    def test_scan_with_filter(self):
        pass

    def test_scan_with_start_key(self):
        db = DB(self.table_name, test=True)

        item = {
            "id": "1",
            "word": "random",
            "number": 42
        }
        db.put(item)
        item = {
            "id": "2",
            "word": "not",
            "number": 36
        }
        db.put(item)

        db_response = db.scan(limit=1)

        self.assertIsNotNone(db_response[1])

        db_response = db.scan(limit=1, start_key=db_response[1])

        self.assertIsNotNone(db_response)
        self.assertIsNotNone(db_response[0])

        items = db_response[0]

        self.assertEqual(1, len(items))
        self.assertIn("id", items[0])
        self.assertEqual("2", items[0]["id"])
        self.assertIn("word", items[0])
        self.assertEqual("not", items[0]["word"])
        self.assertIn("number", items[0])
        self.assertEqual(36, items[0]["number"])

if __name__ == "__main__":
    unittest.main()

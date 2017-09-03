import unittest
import boto3

# Get the service resource.
dynamodb = boto3.resource("dynamodb", region_name="eu-west-1", endpoint_url="http://localhost:8000",
                          aws_access_key_id="anything", aws_secret_access_key="anything")

def setup_dynamo_db(table_name):
    # Create the DynamoDB table.
    table = dynamodb.create_table(
        TableName="alexa_info",
        KeySchema=[
            {
                "AttributeName": "session_id",
                "KeyType": "HASH"
            },
            {
                "AttributeName": "first_name",
                "KeyType": "RANGE"
            }
        ],
        AttributeDefinitions=[
            {
                "AttributeName": "session_id",
                "AttributeType": "S"
            },
            {
                "AttributeName": "first_name",
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
    print "DynamoDB table created"

def tear_down_dynamo_db(table_name):
    table = dynamodb.Table(table_name)
    table.delete()

class DB(unittest.TestCase):
    def setUp(self):
        print "==== Start test ===="
        setup_dynamo_db("TestDB")

    def tearDown(self):
        tear_down_dynamo_db("TestDB")
        print "==== End test ====\n"

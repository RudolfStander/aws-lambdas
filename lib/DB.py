import boto3
from boto3.dynamodb.conditions import Key, Attr

__author__ = 'Rudolf Stander'
__contact__ = 'rudolfstan@gmail.com'
__see__ = 'https://github.com/RudolfStander/aws-lambdas'

def parse_filter_expression(filter_expression):
    # TODO: parse the map based expression and return an expression using
    #       boto3's Key and Attr classes
    return ""

class DB:
    """
    TODO: comment
    """

    def __init__(self, table_name=None, test=False):
        if test:
            self.dynamodb = boto3.resource("dynamodb", region_name="eu-west-1", endpoint_url="http://localhost:8000",
                                           aws_access_key_id="anything", aws_secret_access_key="anything")
        else:
            self.dynamodb = boto3.resource("dynamodb", region_name="eu-west-1")

        if not table_name is None:
            self.table = self.dynamodb.Table(table_name)

    def setup_table(self, table_name):
        if table_name is None or not table_name:
            raise UnboundLocalError("Invalid table name")

        self.table = self.dynamodb.Table(table_name)

    def get(self, key):
        if key is None or not key:
            raise UnboundLocalError("Invalid key")

        db_response = self.table.get_item(Key=key)

        if db_response is None:
            return None
        if not "Item" in db_response:
            return None

        return db_response["Item"]

    def scan(self, limit=None, filter_expression=None, start_key=None):
        args = {}

        if not limit is None:
            args["Limit"] = limit
        if not filter_expression is None:
            raise NotImplementedError("TODO")
            # args["FilterExpression"] = parse_filter_expression(filter_expression)
        if not start_key is None:
            args["ExclusiveStartKey"] = start_key

        db_response = self.table.scan(Select="ALL_ATTRIBUTES", **args)

        if db_response is None:
            return None
        if not "Items" in db_response:
            return None
        if not "LastEvaluatedKey" in db_response:
            return (db_response["Items"], None)
        else:
            return (db_response["Items"], db_response["LastEvaluatedKey"])

    def search(self, params):
        # TODO: search using params
        raise NotImplementedError("TODO")

    def create(self, item):
        # TODO: use condition to block the overwriting of an existing entry
        raise NotImplementedError("TODO")
        
    def put(self, item):
        return self.table.put_item(Item=item)

    def update(self, item):
        # TODO: implement updating using update expressions
        raise NotImplementedError("TODO")

    def delete(self, key):
        return self.table.delete_item(Key=key)

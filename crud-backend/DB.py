from ..lib.ResponseBuilder import ResponseBuilder
from ..lib.RequestHandler import RequestHandler

import boto3

class DB:
    def __init__(self, table_name=None, test=False):
        if test:
            self.dynamodb = boto3.resource("dynamodb", region_name="eu-west-1", endpoint_url="http://localhost:8000",
                                           aws_access_key_id="anything", aws_secret_access_key="anything")
        else:
            self.dynamodb = boto3.resource("dynamodb", region_name="eu-west-1")

        if not table_name is None:
            self.table = self.dynamodb.Table(table_name)

    def setup_table(self, table_name):
        if table_name is None:
            raise UnboundLocalError("Table name is empty")

        self.table = self.dynamodb.Table(table_name)

    def get(self, key={}):
        db_response = self.table.get_item(Key=key)

        if db_response is None:
            return None
        if not "Item" in db_response:
            return None
        
        return db_response["Item"]

    def get_all(self, limit=None):
        db_response = self.table.scan(Select="ALL_ATTRIBUTES")

        if db_response is None:
            return None
        if not "Items" in db_response:
            return None

        return db_response["Items"]

    def create(self, item):
        return self.table.put_item(Item=item)

    def update(self, item):
        # TODO: check if there is a proper way of updating
        raise NotImplementedError("TODO")

    def delete(self, key):
        # TODO: check how to delete
        raise NotImplementedError("TODO")

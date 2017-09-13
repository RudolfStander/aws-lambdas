from .CRUDHandler import CRUDHandler

def lambda_handler(request, context):
    handler = CRUDHandler(table_name="TestDB")
    return handler.handle(request)

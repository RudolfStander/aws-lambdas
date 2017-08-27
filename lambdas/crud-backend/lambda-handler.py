from .CRUDHandler import CRUDHandler

def lambda_handler(request, context):
    handler = CRUDHandler("some_table_name")
    return handler.handle(request)

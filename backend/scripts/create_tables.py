import boto3
import os
from dotenv import load_dotenv

load_dotenv()

region = os.getenv('AWS_REGION', 'us-east-1')
endpoint_url = os.getenv('DYNAMODB_ENDPOINT_URL')

session = boto3.session.Session(region_name=region)
dynamodb = session.client('dynamodb', endpoint_url=endpoint_url)

def create_table(table_name, key_schema, attribute_definitions, billing_mode='PAY_PER_REQUEST'):
    try:
        dynamodb.describe_table(TableName=table_name)
        print(f"Table {table_name} already exists")
        return
    except dynamodb.exceptions.ResourceNotFoundException:
        pass

    params = {
        'TableName': table_name,
        'KeySchema': key_schema,
        'AttributeDefinitions': attribute_definitions,
        'BillingMode': billing_mode,
    }
    resp = dynamodb.create_table(**params)
    print(f"Creating {table_name}... status: {resp['TableDescription']['TableStatus']}")

if __name__ == '__main__':
    create_table(
        'cs_users',
        key_schema=[{'AttributeName': 'email', 'KeyType': 'HASH'}],
        attribute_definitions=[{'AttributeName': 'email', 'AttributeType': 'S'}],
    )
    create_table(
        'cs_service_requests',
        key_schema=[{'AttributeName': 'request_id', 'KeyType': 'HASH'}],
        attribute_definitions=[{'AttributeName': 'request_id', 'AttributeType': 'S'}],
    )
    create_table(
        'cs_bills',
        key_schema=[{'AttributeName': 'bill_id', 'KeyType': 'HASH'}],
        attribute_definitions=[{'AttributeName': 'bill_id', 'AttributeType': 'S'}],
    )
    create_table(
        'cs_payments',
        key_schema=[{'AttributeName': 'payment_id', 'KeyType': 'HASH'}],
        attribute_definitions=[{'AttributeName': 'payment_id', 'AttributeType': 'S'}],
    )
    print('Done.')

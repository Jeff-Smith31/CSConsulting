from .config import settings

_session = None
_dynamodb = None
_dynamodb_client = None

USERS_TABLE = "cs_users"
SERVICE_REQUESTS_TABLE = "cs_service_requests"
BILLS_TABLE = "cs_bills"
PAYMENTS_TABLE = "cs_payments"


def _require_boto3():
    try:
        import boto3  # type: ignore
        return boto3
    except Exception as e:
        raise RuntimeError(
            "boto3 is required for DynamoDB operations but is not installed. "
            "Install dependencies with 'pip install -r backend/requirements.txt' or 'pip install boto3'."
        ) from e


def get_boto3_session():
    global _session
    if _session is None:
        boto3 = _require_boto3()
        kwargs = {"region_name": settings.aws_region}
        if settings.aws_access_key_id and settings.aws_secret_access_key:
            kwargs.update(
                {
                    "aws_access_key_id": settings.aws_access_key_id,
                    "aws_secret_access_key": settings.aws_secret_access_key,
                }
            )
        _session = boto3.session.Session(**kwargs)
    return _session


def get_dynamodb():
    global _dynamodb
    if _dynamodb is None:
        session = get_boto3_session()
        _dynamodb = session.resource(
            "dynamodb", endpoint_url=settings.dynamodb_endpoint_url
        )
    return _dynamodb


def get_dynamodb_client():
    global _dynamodb_client
    if _dynamodb_client is None:
        session = get_boto3_session()
        _dynamodb_client = session.client(
            "dynamodb", endpoint_url=settings.dynamodb_endpoint_url
        )
    return _dynamodb_client


def get_table(name: str):
    return get_dynamodb().Table(name)


def _ensure_table(client, table_name: str, key_attr: str):
    try:
        client.describe_table(TableName=table_name)
        return False  # already exists
    except client.exceptions.ResourceNotFoundException:
        pass
    client.create_table(
        TableName=table_name,
        BillingMode="PAY_PER_REQUEST",
        KeySchema=[{"AttributeName": key_attr, "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": key_attr, "AttributeType": "S"}],
    )
    waiter = client.get_waiter("table_exists")
    waiter.wait(TableName=table_name)
    return True


def ensure_tables_if_not_exist() -> dict:
    """Create required DynamoDB tables if they do not exist. Returns a summary dict."""
    client = get_dynamodb_client()
    created = {}
    created[USERS_TABLE] = _ensure_table(client, USERS_TABLE, "email")
    created[SERVICE_REQUESTS_TABLE] = _ensure_table(client, SERVICE_REQUESTS_TABLE, "request_id")
    created[BILLS_TABLE] = _ensure_table(client, BILLS_TABLE, "bill_id")
    created[PAYMENTS_TABLE] = _ensure_table(client, PAYMENTS_TABLE, "payment_id")
    return created

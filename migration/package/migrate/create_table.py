import boto3


def create_table(t_name, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.create_table(
            AttributeDefinitions=[
                {
                    "AttributeName": "dumy",
                    "AttributeType": "N",
                },
                {
                    "AttributeName": "id",
                    "AttributeType": "S",
                },
                {
                    "AttributeName": "title",
                    "AttributeType": "S",
                },
                {
                    "AttributeName": "score",
                    "AttributeType": "N",
                },
                {
                    "AttributeName": "desc",
                    "AttributeType": "S",
                },
            ],
            KeySchema=[
                {
                    "AttributeName": "dumy",
                    "KeyType": "HASH",
                },
                {
                    "AttributeName": "id",
                    "KeyType": "RANGE",
                },
            ],
            BillingMode="PAY_PER_REQUEST",
            LocalSecondaryIndexes=[
                {
                    "IndexName": "title-index",
                    "KeySchema": [
                        {
                            "AttributeName": "dumy",
                            "KeyType": "HASH",
                        },
                        {
                            "AttributeName": "title",
                            "KeyType": "RANGE",
                        },
                    ],
                    "Projection": {
                        "ProjectionType": "ALL",
                    },
                },
                {
                    "IndexName": "score-index",
                    "KeySchema": [
                        {
                            "AttributeName": "dumy",
                            "KeyType": "HASH",
                        },
                        {
                            "AttributeName": "score",
                            "KeyType": "RANGE",
                        },
                    ],
                    "Projection": {
                        "ProjectionType": "ALL",
                    },
                },
                {
                    "IndexName": "desc-index",
                    "KeySchema": [
                        {
                            "AttributeName": "dumy",
                            "KeyType": "HASH",
                        },
                        {
                            "AttributeName": "desc",
                            "KeyType": "RANGE",
                        },
                    ],
                    "Projection": {
                        "ProjectionType": "ALL",
                    },
                },
            ],
            TableName=t_name,
            StreamSpecification={
                "StreamEnabled": False,
            },
        )
        return table

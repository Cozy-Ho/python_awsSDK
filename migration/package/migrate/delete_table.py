import boto3

client = boto3.client('dynamodb')


def delete_table(t_name, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')
    try:
        response = client.delete_table(
            TableName=t_name
        )
    except Exception as e:
        print(e)
        return e

    return "done"

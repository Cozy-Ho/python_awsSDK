import boto3
import json
import decimal
import numpy as np


class DecimalEncoder(json.JSONEncoder):
    # Json parsing error 때문에 받아온 데이터의 타입에따라 처리 방법을 새로 정의 해 줬다.
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return int(o)
        if isinstance(o, set):  # <---resolving sets as lists
            return list(o)
        return super(DecimalEncoder, self).default(o)


def write_file(file_path, data):
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, cls=DecimalEncoder)


def export_data(t_name, file_path, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(t_name)
    params = {}
    done = False
    start_key = None
    movies = []
    try:
        while not done:
            if start_key:
                params['ExclusiveStartKey'] = start_key
            response = table.scan(**params)
            for item in response.get("Items"):
                movies.append(item)
            start_key = response.get('LastEvaluatedKey', None)
            done = start_key is None
        # print(movies)
        # movies = np.array(movies)
        # movies = movies.flatten()
        # movies = movies.tolist()
        write_file(file_path, movies)
    except Exception as e:
        print(e)
        return False

    return True

import boto3
import json


def read_file(file_path):
    with open(file_path, "r") as json_file:
        return json.load(json_file)


def make_query(data, t_name):
    ret_arr = []
    sub = []
    for movie in data:
        sub.append({
            "PutRequest": {
                "Item": movie
            }
        })
        if(len(sub) == 25):
            ret_arr.append(sub)
            sub.clear()
    if len(sub) > 0:
        ret_arr.append(sub)
    return ret_arr


def import_data(t_name, file_path, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')
        client = boto3.client('dynamodb')
        table = dynamodb.Table(t_name)

    try:
        print("READING FILE >>> ")
        data = read_file(file_path)
        queries = make_query(data, t_name)
        print("QUERY is READY >>> ")
        i = 0
        with table.batch_writer() as batch:
            for query in data:
                batch.put_item(Item=query)
                if i % 25 == 0:
                    print(i)
                i += 1
        print("Import DONE")
        return "done"

    except Exception as e:
        print(e)
        return e

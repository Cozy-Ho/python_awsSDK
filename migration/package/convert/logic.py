import json
import decimal


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


def add(file_path):
    try:

        with open(file_path, "r") as json_file:
            data = json.load(json_file)
            # print(data)
            # print(data[0])
            data.append({"dumy": 123, "id": "test",
                         "score": 0, "title": "wow", "favorite": "soso"})
            write_file(file_path, data)
            return "done"
    except Exception as e:
        print(e)
        return e


def delete(file_path):
    try:
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
            for movie in data:
                movie.pop('score', None)
            write_file(file_path, data)
        return "done"
    except Exception as e:
        print(e)
        return e


def update(file_path):
    try:
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
            for movie in data:
                if movie["score"] > 50:
                    movie["favorite"] = "good"
                else:
                    movie["favorite"] = "soso"
            write_file(file_path, data)
        return "done"
    except Exception as e:
        print(e)
        return e


if __name__ == "__main__":
    pass

import json


def add(file_path):
    with open(file_path, "r") as json_file:
        data = json.load(json_file)
        print(data)
        return True


if __name__ == "__main__":
    pass

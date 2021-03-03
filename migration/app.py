from pprint import pprint
from package.migrate import *
import time
import os
# 패키지 구조가 안익숙해서 그런가 아직 사용법이 완전하지 않다.
# from boto3.dynamodb.conditions import Key

# client = boto3.client('dynamodb')

cur_dir = os.path.dirname(__file__)


def print_manual():
    print("=====================================")
    print("1 : Create TEST Table")
    print("2 : Delete Table")
    print("3 : Export Data")
    print("4 : Import Data")
    print("5 : Convert Data")
    print("0 : EXIT_PORGRAM")
    print("=====================================")
    print("명령어를 입력하세요 ( 0 ~ 5 )")
    print("=====================================")


if __name__ == "__main__":
    flag = True
    while(flag):
        print_manual()
        input_command = input("COMMAND >>> ")
        if input_command == "1":
            t_name = input("tablename >>> ")
            result = create_table.create_table(t_name)
            print(result)
        elif input_command == "2":
            t_name = input("tablename >>> ")
            result = delete_table.delete_table(t_name)
            if(result):
                print(result)
        elif input_command == "3":
            t_name = input("tablename >>> ")
            file_name = input("file_name >>> ")
            file_path = os.path.join(cur_dir, f"json_data/{file_name}.json")
            start = time.time()
            result = export_data.export_data(t_name, file_path)
            print("EXPORT TIME >>> ", time.time() - start)
        elif input_command == "4":
            t_name = input("tablename >>> ")
            file_name = input("file_name >>> ")
            file_path = os.path.join(cur_dir, f"json_data/{file_name}.json")
            start = time.time()
            result = import_data.import_data(t_name, file_path)
            print("IMPORT TIME >>> ", time.time() - start)
        elif input_command == "5":
            pass
        elif input_command == "0":
            flag = False

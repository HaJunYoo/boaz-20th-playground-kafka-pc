from kafka import KafkaConsumer
import json
import os
import csv
import time


class Consumer:
    def __init__(self, brokers, topicName):
        self.consumer = KafkaConsumer(
            topicName,
            bootstrap_servers=brokers,
            api_version=(0, 11, 5)
        )
        self.time_limit = 10  # 10초 제한시간 설정

    def income_check(self):
        print("Start income check")

        start_time = time.time()  # 시작 시간 기록

        for idx, message in enumerate(self.consumer):
            data = json.loads(message.value.decode())

            # 종료 신호를 받으면 종료
            if data == "DONE":
                print("Received done signal, exiting...")
                break

            index = data['index']
            row = data['row']
            # income이 $120K 이상인 경우
            if "$120K +" in str(row[7]):
                print("--income exceeds $120K")
                # CLIENTNUM, Customer_Age, Gender, Dependent_count, Education_Level, Marital_Status, Income_Category, Card_Category 정보만 저장
                new_row = [row[0], row[2], row[3], row[4], row[5], row[6], row[7], row[8]]
                rows_to_write.append(new_row)
                print(f'{index}번째 데이터 => {new_row.__str__()}')

        print("End income check")

        print("write to csv file")
        # 새로운 csv 파일에 쓰기
        file_name = "./high_income_customers.csv"
        file_path = os.path.join(os.path.dirname(__file__), file_name)
        with open(file_path, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(
                ['CLIENTNUM', 'Customer_Age', 'Gender', 'Dependent_count', 'Education_Level', 'Marital_Status',
                 'Income_Category', 'Card_Category'])
            writer.writerows(rows_to_write)
        print("write to csv file done")


if __name__ == '__main__':
    brokers = ["localhost:9092"]
    topicName = "bank"
    consumer = Consumer(brokers, topicName)
    rows_to_write = []  # 새로운 csv 파일에 쓸 row 저장
    consumer.income_check()

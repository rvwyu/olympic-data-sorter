import csv

def read_csv_file(file_name):
    data_set = []
    with open(file_name, mode='r', encoding="utf-8") as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data_set.append(row)
    return data_set

def write_csv_file(file_name, data_set):
    with open(file_name, mode='w', newline='', encoding="utf-8") as file:
        csv_writer = csv.writer(file)
        for row in data_set:
            csv_writer.writerow(row)
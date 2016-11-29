"""
Prepare.py
Prepares the dataset..Merges all the dataset to create one
master dataset
"""
import csv
from collections import defaultdict
from functions import get_box_index

def load_from_csv(filename, lat_index, long_index):
    first = False
    with open('data/'+filename, 'r') as csvfile:
        service_reader = csv.reader(csvfile)
        for row in service_reader:
            if not first:
                first = True
                continue
            try:
                latitude = row[lat_index].strip()
                longitude = row[long_index].strip()

                if len(latitude) < 5 or len(longitude) < 5:
                    continue
                # print(latitude, " and ", longitude)
                latitude = float(latitude)
                longitude = float(longitude)

                index = get_box_index(latitude, longitude)
                yield index, row
            except:
                raise

def load_service_requests(master_dataset):
    for index, row in load_from_csv('service_requests.csv', 13, 14):
        master_dataset[index]["services"] += 1
    print("Service requests loaded")

def prepare_dataset():
    master_table = defaultdict(lambda :defaultdict(int))
    load_service_requests(master_table)

    # Write the master table in csv file
    print("Writing into output file")
